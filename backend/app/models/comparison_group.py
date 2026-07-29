# backend/app/models/comparison_group.py

from datetime import datetime
from app.extensions import db


class ComparisonGroup(db.Model):
    """
    Groups multiple Experiments run together for side-by-side comparison.
    One ComparisonGroup -> many Experiments (same dataset, different algorithms).
    """
    __tablename__ = "comparison_groups"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    dataset_label = db.Column(db.String(120), nullable=False)
    dataset_source = db.Column(db.String(20), nullable=False)   # "builtin" | "uploaded"
    task_type = db.Column(db.String(50), nullable=False)        # all children share this

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    experiments = db.relationship(
        "Experiment", backref="comparison_group",
        lazy="dynamic", cascade="all, delete-orphan"
    )

    def to_dict(self, include_experiments=True) -> dict:
        data = {
            "id": self.id,
            "dataset_label": self.dataset_label,
            "dataset_source": self.dataset_source,
            "task_type": self.task_type,
            "created_at": self.created_at.isoformat(),
        }
        if include_experiments:
            data["experiments"] = [e.to_dict() for e in self.experiments.order_by("id")]
        return data

    def __repr__(self) -> str:
        return f"<ComparisonGroup {self.dataset_label} ({self.task_type})>"