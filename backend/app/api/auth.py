from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.utils.schemas import register_schema, login_schema
from app.services.auth_service import AuthService

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    # 1. Validate input (raises ValidationError automatically if invalid)
    data = register_schema.load(request.get_json())

    # 2. Call service — all logic lives there
    result = AuthService.register_user(
        username=data["username"],
        email=data["email"],
        password=data["password"]
    )

    # 3. Return response
    return jsonify(result), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = login_schema.load(request.get_json())

    result = AuthService.login_user(
        email=data["email"],
        password=data["password"]
    )

    return jsonify(result), 200


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def get_me():
    user_id = get_jwt_identity()
    user = AuthService.get_current_user(int(user_id))
    return jsonify(user.to_dict()), 200


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    user_id = get_jwt_identity()
    result = AuthService.refresh_access_token(int(user_id))
    return jsonify(result), 200