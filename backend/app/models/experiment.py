from datetime import datetime
from app.extensions import db


class ExperimentStatus:
    """
    Constants class — avoids magic strings scattered in code.
    Instead of writing "pending" everywhere, write ExperimentStatus.PENDING
    """
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class Experiment(db.Model):
    __tablename__ = "experiments"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    dataset_id = db.Column(
        db.Integer,
        db.ForeignKey("datasets.id", ondelete="SET NULL"),
        nullable=True   # nullable because built-in datasets aren't stored as rows
    )

    comparison_group_id = db.Column(
    db.Integer,
    db.ForeignKey("comparison_groups.id", ondelete="CASCADE"),
    nullable=True   # null = standalone experiment from Studio
)

    # Algorithm details
    algorithm_name = db.Column(db.String(100), nullable=False)  # "naive_bayes"
    algorithm_display_name = db.Column(db.String(100), nullable=False)  # "Naive Bayes"
    parameters = db.Column(db.JSON, nullable=True)   # hyperparameters the user chose
    task_type = db.Column(db.String(50), nullable=False)  # "classification" / "clustering"

    # Execution
    status = db.Column(
        db.String(20),
        default=ExperimentStatus.PENDING,
        nullable=False
    )
    celery_task_id = db.Column(db.String(255), nullable=True)  # for async tracking
    error_message = db.Column(db.Text, nullable=True)          # if status = failed

    # Results — stored as JSON (metrics, charts data, etc.)
    result = db.Column(db.JSON, nullable=True)

    # Timing
    started_at = db.Column(db.DateTime, nullable=True)
    completed_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    @property
    def duration_seconds(self) -> float | None:
        """Computed property — not stored in DB, calculated on the fly."""
        if self.started_at and self.completed_at:
            return (self.completed_at - self.started_at).total_seconds()
        return None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "algorithm_name": self.algorithm_name,
            "algorithm_display_name": self.algorithm_display_name,
            "parameters": self.parameters,
            "task_type": self.task_type,
            "status": self.status,
            "celery_task_id": self.celery_task_id,
            "result": self.result,
            "error_message": self.error_message,
            "duration_seconds": self.duration_seconds,
            "created_at": self.created_at.isoformat(),
            "dataset_id": self.dataset_id,
            "comparison_group_id": self.comparison_group_id,
        }

    def __repr__(self) -> str:
        return f"<Experiment {self.algorithm_name} [{self.status}]>"