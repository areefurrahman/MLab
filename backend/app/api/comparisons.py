# backend/app/api/comparisons.py

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.utils.schemas import run_comparison_schema
from app.services.comparison_service import ComparisonService

comparisons_bp = Blueprint("comparisons", __name__)


@comparisons_bp.route("/run", methods=["POST"])
@jwt_required()
def run_comparison():
    user_id = int(get_jwt_identity())
    data = run_comparison_schema.load(request.get_json())

    group = ComparisonService.create_comparison(
        user_id=user_id,
        algorithm_names=data["algorithm_names"],
        dataset_source=data["dataset_source"],
        dataset_key=data.get("dataset_key"),
        dataset_id=data.get("dataset_id"),
        target_column=data.get("target_column"),
    )
    return jsonify(group.to_dict()), 202


@comparisons_bp.route("/<int:group_id>", methods=["GET"])
@jwt_required()
def get_comparison(group_id):
    user_id = int(get_jwt_identity())
    group = ComparisonService.get_comparison_or_404(group_id, user_id)
    return jsonify(group.to_dict()), 200


@comparisons_bp.route("", methods=["GET"])
@jwt_required()
def list_comparisons():
    user_id = int(get_jwt_identity())
    return jsonify(ComparisonService.get_user_comparisons(user_id)), 200