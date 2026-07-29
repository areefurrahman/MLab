# backend/app/api/experiments.py

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.extensions import db
from app.utils.schemas import run_experiment_schema
from app.services.experiment_service import ExperimentService
from app.tasks.experiment_tasks import run_experiment_task

experiments_bp = Blueprint("experiments", __name__)


@experiments_bp.route("/run", methods=["POST"])
@jwt_required()
def run_experiment():
    user_id = int(get_jwt_identity())
    data = run_experiment_schema.load(request.get_json())

    # 1. Create the experiment row instantly (status = pending)
    experiment = ExperimentService.create_pending_experiment(
        user_id=user_id,
        algorithm_name=data["algorithm_name"],
        dataset_source=data["dataset_source"],
        dataset_key=data.get("dataset_key"),
        dataset_id=data.get("dataset_id"),
        target_column=data.get("target_column"),
        items_column=data.get("items_column"),
        parameters=data.get("parameters", {}),
    )

    # 2. Hand off to Celery — returns immediately, doesn't wait
    task = run_experiment_task.delay(experiment.id)
    experiment.celery_task_id = task.id
    db.session.commit()

    # 3. Respond NOW with status=pending — frontend will poll for completion
    return jsonify(experiment.to_dict()), 202


@experiments_bp.route("", methods=["GET"])
@jwt_required()
def list_experiments():
    user_id = int(get_jwt_identity())
    return jsonify(ExperimentService.get_user_experiments(user_id)), 200


@experiments_bp.route("/<int:experiment_id>", methods=["GET"])
@jwt_required()
def get_experiment(experiment_id):
    user_id = int(get_jwt_identity())
    experiment = ExperimentService.get_experiment_or_404(experiment_id, user_id)
    return jsonify(experiment.to_dict()), 200