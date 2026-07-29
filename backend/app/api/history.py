# backend/app/api/history.py

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.history_service import HistoryService

history_bp = Blueprint("history", __name__)

VALID_TYPES = {"experiment", "comparison", "inference"}
VALID_STATUSES = {"pending", "running", "completed", "failed"}


@history_bp.route("", methods=["GET"])
@jwt_required()
def get_history():
    user_id = int(get_jwt_identity())

    type_filter = request.args.get("type")
    status_filter = request.args.get("status")

    if type_filter and type_filter not in VALID_TYPES:
        return jsonify({"error": f"Invalid type. Must be one of: {', '.join(VALID_TYPES)}"}), 422

    if status_filter and status_filter not in VALID_STATUSES:
        return jsonify({"error": f"Invalid status. Must be one of: {', '.join(VALID_STATUSES)}"}), 422

    items = HistoryService.get_unified_history(user_id, type_filter, status_filter)
    return jsonify(items), 200


@history_bp.route("/experiment/<int:item_id>", methods=["GET"])
@jwt_required()
def get_experiment_detail(item_id):
    user_id = int(get_jwt_identity())
    return jsonify(HistoryService.get_experiment_detail(item_id, user_id)), 200


@history_bp.route("/comparison/<int:item_id>", methods=["GET"])
@jwt_required()
def get_comparison_detail(item_id):
    user_id = int(get_jwt_identity())
    return jsonify(HistoryService.get_comparison_detail(item_id, user_id)), 200


@history_bp.route("/inference/<int:item_id>", methods=["GET"])
@jwt_required()
def get_inference_detail(item_id):
    user_id = int(get_jwt_identity())
    return jsonify(HistoryService.get_inference_detail(item_id, user_id)), 200