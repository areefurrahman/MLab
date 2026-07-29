# backend/app/services/history_service.py

from sqlalchemy.orm import defer
from app.models import Experiment, ComparisonGroup, InferenceRun
from app.utils.exceptions import NotFoundError


class HistoryService:

    @staticmethod
    def get_unified_history(user_id: int, type_filter: str = None, status_filter: str = None) -> list:
        items = []

        # ── Standalone Experiments ────────────────────────────────────────────────
        if type_filter in (None, "experiment"):
            experiments = Experiment.query.filter(
                Experiment.user_id == user_id,
                Experiment.comparison_group_id.is_(None)
            ).all()   # ← no ORDER BY — Python sorts at the end

            for exp in experiments:
                if status_filter and exp.status != status_filter:
                    continue
                items.append(HistoryService._normalize_experiment(exp))

        # ── Comparison Groups ─────────────────────────────────────────────────────
        if type_filter in (None, "comparison"):
            groups = ComparisonGroup.query.filter_by(
                user_id=user_id
            ).all()   # ← no ORDER BY

            for group in groups:
                overall_status = HistoryService._group_status(group)
                if status_filter and overall_status != status_filter:
                    continue
                items.append(HistoryService._normalize_group(group, overall_status))

        # ── Inference Runs ────────────────────────────────────────────────────────
        if type_filter in (None, "inference"):
            # defer(output_data) — tells SQLAlchemy NOT to load that column
            # in this query. output_data holds base64 audio/images — megabytes
            # per row. We only need metadata for the list view.
            runs = InferenceRun.query.options(
                defer(InferenceRun.output_data)
            ).filter_by(
                user_id=user_id
            ).all()   # ← no ORDER BY

            for run in runs:
                if status_filter and run.status != status_filter:
                    continue
                items.append(HistoryService._normalize_inference(run))

        # Single sort in Python covers all three streams correctly
        items.sort(key=lambda x: x["created_at"], reverse=True)
        return items

    # ── Normalizers — give every item the same shape ──────────────────────────

    @staticmethod
    def _normalize_experiment(exp: Experiment) -> dict:
        metrics = exp.result.get("metrics", {}) if exp.result else {}
        accuracy = metrics.get("accuracy")
        return {
            "id": exp.id,
            "type": "experiment",
            "title": f"{exp.algorithm_display_name}",
            "subtitle": f"Standalone · {exp.task_type}",
            "status": exp.status,
            "created_at": exp.created_at.isoformat(),
            "duration_seconds": exp.duration_seconds,
            "summary": {
                "algorithm": exp.algorithm_display_name,
                "task_type": exp.task_type,
                "accuracy": round(accuracy * 100, 1) if accuracy is not None else None,
                "rule_count": exp.result.get("rule_count") if exp.result else None,
            },
            "detail_url": f"/history/experiment/{exp.id}",
        }

    @staticmethod
    def _normalize_group(group: ComparisonGroup, status: str) -> dict:
        experiments = group.experiments.all()   # ← .all() on dynamic relationship
        algo_names = [e.algorithm_display_name for e in experiments]
        return {
            "id": group.id,
            "type": "comparison",
            "title": f"Compare: {', '.join(algo_names)}",
            "subtitle": f"{group.dataset_label} · {group.task_type}",
            "status": status,
            "created_at": group.created_at.isoformat(),
            "duration_seconds": None,
            "summary": {
                "algorithm_count": len(experiments),
                "dataset": group.dataset_label,
                "task_type": group.task_type,
            },
            "detail_url": f"/history/comparison/{group.id}",
        }

    @staticmethod
    def _normalize_inference(run: InferenceRun) -> dict:
        summary = {}
        if run.output_data:
            if run.task_name == "ner":
                summary["entity_count"] = run.output_data.get("entity_count")
            elif run.task_name == "text_generation":
                prompt = run.output_data.get("prompt", "")
                summary["prompt_preview"] = prompt[:60] + "..." if len(prompt) > 60 else prompt
            elif run.task_name == "voice_qa":
                summary["question"] = run.output_data.get("transcribed_question", "")
            elif run.task_name == "cnn_gender":
                summary["predicted_label"] = run.output_data.get("predicted_label")
                summary["confidence"] = run.output_data.get("confidence")

        return {
            "id": run.id,
            "type": "inference",
            "title": run.task_display_name,
            "subtitle": f"Inference · {run.category.replace('_', ' ')}",
            "status": run.status,
            "created_at": run.created_at.isoformat(),
            "duration_seconds": run.duration_seconds,
            "summary": summary,
            "detail_url": f"/history/inference/{run.id}",
        }

    @staticmethod
    def _group_status(group: ComparisonGroup) -> str:
        statuses = {e.status for e in group.experiments.all()}   # ← .all() here too
        if "failed" in statuses and len(statuses) == 1:
            return "failed"
        if statuses == {"completed"}:
            return "completed"
        if "running" in statuses or "pending" in statuses:
            return "running"
        return "completed"

    # ── Detail fetchers (reuse existing service logic) ────────────────────────

    @staticmethod
    def get_experiment_detail(experiment_id: int, user_id: int) -> dict:
        exp = Experiment.query.filter_by(id=experiment_id, user_id=user_id).first()
        if not exp:
            raise NotFoundError("Experiment not found")
        return exp.to_dict()

    @staticmethod
    def get_comparison_detail(group_id: int, user_id: int) -> dict:
        group = ComparisonGroup.query.filter_by(id=group_id, user_id=user_id).first()
        if not group:
            raise NotFoundError("Comparison not found")
        return group.to_dict()

    @staticmethod
    def get_inference_detail(run_id: int, user_id: int) -> dict:
        run = InferenceRun.query.filter_by(id=run_id, user_id=user_id).first()
        if not run:
            raise NotFoundError("Inference run not found")
        return run.to_dict()
    




