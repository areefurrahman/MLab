# backend/app/api/datasets.py  (new blueprint)

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.ml.datasets import BuiltinDatasetRegistry
from app.services.dataset_service import DatasetService

datasets_bp = Blueprint("datasets", __name__)


@datasets_bp.route("/builtin", methods=["GET"])
def list_builtin_datasets():
    return jsonify(BuiltinDatasetRegistry.list_metadata()), 200


@datasets_bp.route("/upload", methods=["POST"])
@jwt_required()
def upload_dataset():
    user_id = int(get_jwt_identity())
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    name = request.form.get("name", "")
    result = DatasetService.upload_dataset(user_id, file, name)
    return jsonify(result), 201


@datasets_bp.route("", methods=["GET"])
@jwt_required()
def list_my_datasets():
    user_id = int(get_jwt_identity())
    return jsonify(DatasetService.get_user_datasets(user_id)), 200