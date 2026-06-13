from flask import jsonify
from marshmallow import ValidationError
from app.utils.exceptions import AppError


def register_error_handlers(app):
    """Attach all error handlers to the Flask app."""

    @app.errorhandler(AppError)
    def handle_app_error(error: AppError):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    @app.errorhandler(ValidationError)
    def handle_marshmallow_error(error: ValidationError):
        return jsonify({"error": "Validation failed", "details": error.messages}), 422

    @app.errorhandler(404)
    def handle_404(error):
        return jsonify({"error": "Endpoint not found"}), 404

    @app.errorhandler(500)
    def handle_500(error):
        return jsonify({"error": "Internal server error"}), 500