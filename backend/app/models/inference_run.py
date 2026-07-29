# backend/app/models/inference_run.py

from datetime import datetime
from app.extensions import db


class InferenceRun(db.Model):
    __tablename__ = "inference_runs"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    task_name = db.Column(db.String(100), nullable=False)          # "ner"
    task_display_name = db.Column(db.String(100), nullable=False)  # "Named Entity Recognition"
    category = db.Column(db.String(50), nullable=False)            # "deep_learning"

    input_data = db.Column(db.JSON, nullable=True)     # what the user submitted
    output_data = db.Column(db.JSON, nullable=True)    # result from the pipeline
    status = db.Column(db.String(20), default="pending", nullable=False)
    error_message = db.Column(db.Text, nullable=True)
    celery_task_id = db.Column(db.String(255), nullable=True)

    started_at = db.Column(db.DateTime, nullable=True)
    completed_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    @property
    def duration_seconds(self) -> float | None:
        if self.started_at and self.completed_at:
            return round((self.completed_at - self.started_at).total_seconds(), 3)
        return None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "task_name": self.task_name,
            "task_display_name": self.task_display_name,
            "category": self.category,
            "input_data": self.input_data,
            "output_data": self.output_data,
            "status": self.status,
            "error_message": self.error_message,
            "celery_task_id": self.celery_task_id,
            "duration_seconds": self.duration_seconds,
            "created_at": self.created_at.isoformat(),
        }

    def __repr__(self):
        return f"<InferenceRun {self.task_name} [{self.status}]>"