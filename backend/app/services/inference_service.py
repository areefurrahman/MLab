# backend/app/services/inference_service.py

from datetime import datetime
from app.extensions import db
from app.models import InferenceRun
from app.ml.inference_registry import InferenceTaskRegistry
from app.utils.exceptions import NotFoundError


class InferenceService:

    @staticmethod
    def create_pending_run(user_id: int, task_name: str, input_data: dict) -> InferenceRun:
        task_cls = InferenceTaskRegistry.get(task_name)   # validates it exists early

        run = InferenceRun(
            user_id=user_id,
            task_name=task_cls.name,
            task_display_name=task_cls.display_name,
            category=task_cls.category,
            input_data=input_data,
            status="pending",
        )
        db.session.add(run)
        db.session.commit()
        return run

    @staticmethod
    def execute_run(run_id: int) -> dict:
        run = InferenceRun.query.get(run_id)
        if not run:
            raise NotFoundError(f"InferenceRun {run_id} not found")

        try:
            run.status = "running"
            run.started_at = datetime.utcnow()
            db.session.commit()

            task_cls = InferenceTaskRegistry.get(run.task_name)
            task = task_cls()
            output = task.run(run.input_data)

            run.status = "completed"
            run.output_data = output
            run.completed_at = datetime.utcnow()
            db.session.commit()

        except Exception as e:
            run.status = "failed"
            run.error_message = str(e)
            run.completed_at = datetime.utcnow()
            db.session.commit()
            raise

        return run.to_dict()

    @staticmethod
    def get_run_or_404(run_id: int, user_id: int) -> InferenceRun:
        run = InferenceRun.query.filter_by(id=run_id, user_id=user_id).first()
        if not run:
            raise NotFoundError("Inference run not found")
        return run

    @staticmethod
    def get_user_runs(user_id: int) -> list:
        runs = InferenceRun.query.filter_by(user_id=user_id).order_by(InferenceRun.created_at.desc()).all()
        return [r.to_dict() for r in runs]