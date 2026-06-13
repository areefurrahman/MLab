from datetime import datetime
from app.extensions import db


class Dataset(db.Model):
    __tablename__ = "datasets"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    name = db.Column(db.String(120), nullable=False)        # display name
    filename = db.Column(db.String(255), nullable=False)    # stored file path
    original_filename = db.Column(db.String(255), nullable=False)  # what user uploaded
    row_count = db.Column(db.Integer, nullable=False)
    column_count = db.Column(db.Integer, nullable=False)
    columns_info = db.Column(db.JSON, nullable=True)        # {col_name: dtype}
    is_builtin = db.Column(db.Boolean, default=False)       # Iris, Titanic, etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    experiments = db.relationship(
        "Experiment",
        backref="dataset",
        lazy="dynamic"
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "original_filename": self.original_filename,
            "row_count": self.row_count,
            "column_count": self.column_count,
            "columns_info": self.columns_info,
            "is_builtin": self.is_builtin,
            "created_at": self.created_at.isoformat(),
        }

    def __repr__(self) -> str:
        return f"<Dataset {self.name} ({self.row_count} rows)>"