# backend/app/utils/error_handlers.py

from flask import jsonify
from flask_cors import cross_origin
from marshmallow import ValidationError
from app.utils.exceptions import AppError


def register_error_handlers(app):

    @app.errorhandler(AppError)
    def handle_app_error(error: AppError):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        response.headers["Access-Control-Allow-Origin"] = "http://localhost:5173"
        return response

    @app.errorhandler(ValidationError)
    def handle_marshmallow_error(error: ValidationError):
        response = jsonify({"error": "Validation failed", "details": error.messages})
        response.status_code = 422
        response.headers["Access-Control-Allow-Origin"] = "http://localhost:5173"
        return response

    @app.errorhandler(404)
    def handle_404(error):
        response = jsonify({"error": "Endpoint not found"})
        response.status_code = 404
        response.headers["Access-Control-Allow-Origin"] = "http://localhost:5173"
        return response

    @app.errorhandler(500)
    def handle_500(error):
        response = jsonify({"error": "Internal server error"})
        response.status_code = 500
        response.headers["Access-Control-Allow-Origin"] = "http://localhost:5173"
        return response