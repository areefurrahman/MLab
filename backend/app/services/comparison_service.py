# backend/app/services/comparison_service.py

from app.extensions import db
from app.models import ComparisonGroup
from app.ml.registry import AlgorithmRegistry
from app.ml.datasets import BuiltinDatasetRegistry
from app.services.dataset_service import DatasetService
from app.services.experiment_service import ExperimentService
from app.tasks.experiment_tasks import run_experiment_task
from app.utils.exceptions import ValidationAppError, NotFoundError


class ComparisonService:

    @staticmethod
    def create_comparison(user_id, algorithm_names: list, dataset_source,
                           dataset_key=None, dataset_id=None, target_column=None) -> ComparisonGroup:
        if len(algorithm_names) < 2:
            raise ValidationAppError({"algorithm_names": ["Select at least 2 algorithms to compare"]})

        # Resolve up front — fails fast before touching the database
        algo_classes = [AlgorithmRegistry.get(name) for name in algorithm_names]

        # All algorithms must share task_type — comparing classification accuracy
        # against a clustering silhouette score is meaningless
        task_types = {cls.task_type for cls in algo_classes}
        if len(task_types) > 1:
            raise ValidationAppError({
                "algorithm_names": [f"Cannot compare across task types: {', '.join(task_types)}"]
            })
        task_type = task_types.pop()

        dataset_label = ComparisonService._resolve_dataset_label(
            dataset_source, dataset_key, dataset_id, user_id
        )

        group = ComparisonGroup(
            user_id=user_id, dataset_label=dataset_label,
            dataset_source=dataset_source, task_type=task_type,
        )
        db.session.add(group)
        db.session.flush()  # assigns group.id, transaction still open

        experiments = []
        for algo_cls in algo_classes:
            experiment = ExperimentService.create_pending_experiment(
                user_id=user_id, algorithm_name=algo_cls.name,
                dataset_source=dataset_source, dataset_key=dataset_key,
                dataset_id=dataset_id, target_column=target_column,
                parameters={}, comparison_group_id=group.id,
                commit=False,   # batch into one transaction
            )
            experiments.append(experiment)

        db.session.commit()   # ← everything saved atomically, BEFORE any task dispatch

        for experiment in experiments:
            run_experiment_task.delay(experiment.id)   # ← now safe to dispatch

        return group

    @staticmethod
    def _resolve_dataset_label(dataset_source, dataset_key, dataset_id, user_id) -> str:
        if dataset_source == "builtin":
            meta = BuiltinDatasetRegistry.get(dataset_key)(metadata_only=True)
            return meta["name"]
        dataset = DatasetService.get_dataset_or_404(dataset_id, user_id)
        return dataset.name

    @staticmethod
    def get_comparison_or_404(group_id: int, user_id: int) -> ComparisonGroup:
        group = ComparisonGroup.query.filter_by(id=group_id, user_id=user_id).first()
        if not group:
            raise NotFoundError("Comparison not found")
        return group

    @staticmethod
    def get_user_comparisons(user_id: int) -> list:
        groups = ComparisonGroup.query.filter_by(user_id=user_id).order_by(ComparisonGroup.created_at.desc()).all()
        return [g.to_dict(include_experiments=False) for g in groups]