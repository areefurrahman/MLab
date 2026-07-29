# backend/app/services/experiment_service.py

from datetime import datetime
from sklearn.model_selection import train_test_split

from app.extensions import db
from app.models import Experiment, ExperimentStatus
from app.ml.registry import AlgorithmRegistry
from app.ml.datasets import BuiltinDatasetRegistry
from app.ml.metrics import compute_classification_metrics, compute_clustering_metrics
from app.ml.preprocessing import (
    prepare_features_and_target,
    parse_transaction_column,
    encode_transactions,
)
from app.services.dataset_service import DatasetService
from app.utils.exceptions import ValidationAppError, NotFoundError
from app.utils.json_utils import to_json_safe


class ExperimentService:

    @staticmethod
    def create_pending_experiment(user_id, algorithm_name, dataset_source, dataset_key=None,
                                   dataset_id=None, target_column=None, items_column=None,
                                   parameters=None, comparison_group_id=None, commit=True) -> Experiment:
        algo_cls = AlgorithmRegistry.get(algorithm_name)
        parameters = parameters or {}

        experiment = Experiment(
            user_id=user_id, dataset_id=dataset_id,
            algorithm_name=algo_cls.name, algorithm_display_name=algo_cls.display_name,
            parameters=parameters, task_type=algo_cls.task_type,
            status=ExperimentStatus.PENDING,
            comparison_group_id=comparison_group_id,
        )
        experiment.parameters = {
            **parameters,
            "_dataset_source": dataset_source,
            "_dataset_key": dataset_key,
            "_target_column": target_column,
            "_items_column": items_column,
        }
        db.session.add(experiment)

        if commit:
            db.session.commit()
        else:
            db.session.flush()

        return experiment

    @staticmethod
    def execute_experiment(experiment_id: int) -> dict:
        experiment = Experiment.query.get(experiment_id)
        if not experiment:
            raise NotFoundError(f"Experiment {experiment_id} not found")

        try:
            experiment.status = ExperimentStatus.RUNNING
            experiment.started_at = datetime.utcnow()
            db.session.commit()

            algo_cls = AlgorithmRegistry.get(experiment.algorithm_name)
            raw_params = dict(experiment.parameters or {})
            dataset_source = raw_params.pop("_dataset_source", None)
            dataset_key = raw_params.pop("_dataset_key", None)
            target_column = raw_params.pop("_target_column", None)
            items_column = raw_params.pop("_items_column", None)

            if algo_cls.task_type == "association_rules":
                transactions = ExperimentService._load_transactions(
                    dataset_source, dataset_key, experiment.dataset_id,
                    experiment.user_id, items_column
                )
                result = ExperimentService._run_association_rules(algo_cls, raw_params, transactions)

            else:
                X, y, feature_names, target_names = ExperimentService._load_data(
                    dataset_source, dataset_key, experiment.dataset_id,
                    experiment.user_id, target_column, algo_cls.task_type
                )
                if algo_cls.task_type == "clustering":
                    result = ExperimentService._run_clustering(algo_cls, raw_params, X, feature_names)
                else:
                    result = ExperimentService._run_classification(
                        algo_cls, raw_params, X, y, feature_names, target_names
                    )

            experiment.status = ExperimentStatus.COMPLETED
            experiment.result = result
            experiment.completed_at = datetime.utcnow()
            db.session.commit()
            return experiment.to_dict()

        except Exception as e:
            experiment.status = ExperimentStatus.FAILED
            experiment.error_message = str(e)
            experiment.completed_at = datetime.utcnow()
            db.session.commit()
            raise

    # ─── Loaders ───────────────────────────────────────────────
    @staticmethod
    def _load_data(dataset_source, dataset_key, dataset_id, user_id, target_column, task_type):
        if dataset_source == "builtin":
            data = BuiltinDatasetRegistry.get(dataset_key)(metadata_only=False)
            return data["X"], data["y"], data["feature_names"], data["target_names"]

        if dataset_source == "uploaded":
            df = DatasetService.load_dataframe(dataset_id, user_id)
            if task_type == "clustering":
                numeric_df = df.select_dtypes(include="number")
                return numeric_df.values, None, list(numeric_df.columns), None
            if not target_column:
                raise ValidationAppError({"target_column": ["Required for this algorithm"]})
            if target_column not in df.columns:
                raise ValidationAppError({"target_column": ["Column not found in dataset"]})
            return prepare_features_and_target(df, target_column)

        raise ValidationAppError({"dataset_source": ["Must be 'builtin' or 'uploaded'"]})

    @staticmethod
    def _load_transactions(dataset_source, dataset_key, dataset_id, user_id, items_column) -> list:
        if dataset_source == "builtin":
            data = BuiltinDatasetRegistry.get(dataset_key)(metadata_only=False)
            return data["transactions"]

        if dataset_source == "uploaded":
            df = DatasetService.load_dataframe(dataset_id, user_id)
            if not items_column:
                raise ValidationAppError({"items_column": ["Required for association rule mining"]})
            return parse_transaction_column(df, items_column)

        raise ValidationAppError({"dataset_source": ["Must be 'builtin' or 'uploaded'"]})

    # ─── Runners ───────────────────────────────────────────────
    @staticmethod
    def _run_classification(algo_cls, parameters, X, y, feature_names, target_names):
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42,
            stratify=y if len(set(y)) > 1 else None
        )
        algo = algo_cls(**parameters)
        algo.fit(X_train, y_train)
        y_pred = algo.predict(X_test)
        return {
            "metrics": compute_classification_metrics(y_test, y_pred),
            "feature_names": feature_names, "target_names": target_names,
            "train_size": len(X_train), "test_size": len(X_test),
        }

    @staticmethod
    def _run_clustering(algo_cls, parameters, X, feature_names):
        algo = algo_cls(**parameters)
        algo.fit(X)
        labels = algo.model.labels_
        plot_data = None
        if X.shape[1] == 2:
            plot_data = to_json_safe({"x": X[:, 0], "y": X[:, 1], "cluster": labels})
        return {
            "metrics": compute_clustering_metrics(X, labels),
            "feature_names": feature_names, "sample_size": len(X), "plot_data": plot_data,
        }

    @staticmethod
    def _run_association_rules(algo_cls, parameters, transactions: list):
        one_hot_df = encode_transactions(transactions)
        algo = algo_cls(**parameters)
        algo.fit(one_hot_df)

        rules_df = algo.rules
        rules_list = [] if rules_df.empty else [
            {
                "antecedents": sorted(list(row.antecedents)),
                "consequents": sorted(list(row.consequents)),
                "support": round(float(row.support), 4),
                "confidence": round(float(row.confidence), 4),
                "lift": round(float(row.lift), 4),
            }
            for row in rules_df.itertuples()
        ]

        return to_json_safe({
            "rules": rules_list,
            "rule_count": len(rules_list),
            "transaction_count": len(transactions),
            "unique_items": one_hot_df.shape[1],
        })

    # ─── Reads ───────────────────────────────────────────────
    @staticmethod
    def get_user_experiments(user_id: int) -> list:
        experiments = Experiment.query.filter_by(user_id=user_id).order_by(Experiment.created_at.desc()).all()
        return [e.to_dict() for e in experiments]

    @staticmethod
    def get_experiment_or_404(experiment_id: int, user_id: int) -> Experiment:
        experiment = Experiment.query.filter_by(id=experiment_id, user_id=user_id).first()
        if not experiment:
            raise NotFoundError("Experiment not found")
        return experiment