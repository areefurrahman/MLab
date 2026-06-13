from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    # Relationships
    experiments = db.relationship(
        "Experiment",
        backref="user",
        lazy="dynamic",        # doesn't load until accessed
        cascade="all, delete-orphan"  # delete user = delete their experiments
    )
    datasets = db.relationship(
        "Dataset",
        backref="user",
        lazy="dynamic",
        cascade="all, delete-orphan"
    )

    # --- Password methods ---
    def set_password(self, password: str) -> None:
        """Never store plain text. Always hash."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    # --- Serialization ---
    def to_dict(self) -> dict:
        """Safe representation — password_hash is NEVER included."""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat(),
        }

    def __repr__(self) -> str:
        return f"<User {self.username}>"