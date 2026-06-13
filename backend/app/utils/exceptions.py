class AppError(Exception):
    """Base exception for all application-level errors."""
    status_code = 500
    message = "An unexpected error occurred"

    def __init__(self, message: str = None, status_code: int = None):
        super().__init__(message or self.message)
        self.message = message or self.message
        if status_code:
            self.status_code = status_code

    def to_dict(self) -> dict:
        return {"error": self.message}


class ValidationAppError(AppError):
    status_code = 422
    message = "Validation failed"

    def __init__(self, errors: dict):
        self.errors = errors
        super().__init__(message="Validation failed")

    def to_dict(self) -> dict:
        return {"error": self.message, "details": self.errors}


class ConflictError(AppError):
    status_code = 409
    message = "Resource already exists"


class UnauthorizedError(AppError):
    status_code = 401
    message = "Invalid credentials"


class NotFoundError(AppError):
    status_code = 404
    message = "Resource not found"