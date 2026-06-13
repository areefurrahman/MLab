from flask_jwt_extended import create_access_token, create_refresh_token
from app.extensions import db
from app.models import User
from app.utils.exceptions import ConflictError, UnauthorizedError


class AuthService:
    """
    Handles all authentication business logic.
    Routes call these methods — they contain NO logic of their own.
    """

    @staticmethod
    def register_user(username: str, email: str, password: str) -> dict:
        # Check for existing user
        if User.query.filter_by(email=email).first():
            raise ConflictError("Email already registered")

        if User.query.filter_by(username=username).first():
            raise ConflictError("Username already taken")

        # Create user
        user = User(username=username, email=email)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        return AuthService._build_auth_response(user)

    @staticmethod
    def login_user(email: str, password: str) -> dict:
        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            raise UnauthorizedError("Invalid email or password")

        if not user.is_active:
            raise UnauthorizedError("Account is deactivated")

        return AuthService._build_auth_response(user)

    @staticmethod
    def refresh_access_token(user_id: int) -> dict:
        user = User.query.get(user_id)
        if not user:
            raise UnauthorizedError("User no longer exists")

        access_token = create_access_token(identity=str(user.id))
        return {"access_token": access_token}

    @staticmethod
    def get_current_user(user_id: int) -> User:
        user = User.query.get(user_id)
        if not user:
            raise UnauthorizedError("User not found")
        return user

    @staticmethod
    def _build_auth_response(user: User) -> dict:
        """Internal helper — generates token pair + user data."""
        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))

        return {
            "user": user.to_dict(),
            "access_token": access_token,
            "refresh_token": refresh_token,
        }