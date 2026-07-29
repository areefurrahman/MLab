# backend/app/api/inference.py

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.extensions import db
from app.ml.inference_registry import InferenceTaskRegistry
from app.services.inference_service import InferenceService
from app.tasks.inference_tasks import run_inference_task
from app.utils.exceptions import ValidationAppError


import os
import uuid
from werkzeug.utils import secure_filename
from flask import current_app


inference_bp = Blueprint("inference", __name__)


@inference_bp.route("/tasks", methods=["GET"])
def list_tasks():
    """Public endpoint — no auth needed to browse available inference tasks."""
    return jsonify(InferenceTaskRegistry.list_metadata()), 200


@inference_bp.route("/run", methods=["POST"])
@jwt_required()
def run_inference():
    user_id = int(get_jwt_identity())
    body = request.get_json()

    task_name = body.get("task_name")
    input_data = body.get("input_data", {})

    if not task_name:
        raise ValidationAppError({"task_name": ["Required"]})
    if not isinstance(input_data, dict):
        raise ValidationAppError({"input_data": ["Must be a JSON object"]})

    run = InferenceService.create_pending_run(user_id, task_name, input_data)
    task = run_inference_task.delay(run.id)
    run.celery_task_id = task.id
    db.session.commit()

    return jsonify(run.to_dict()), 202


@inference_bp.route("/<int:run_id>", methods=["GET"])
@jwt_required()
def get_run(run_id):
    user_id = int(get_jwt_identity())
    run = InferenceService.get_run_or_404(run_id, user_id)
    return jsonify(run.to_dict()), 200


@inference_bp.route("", methods=["GET"])
@jwt_required()
def list_my_runs():
    user_id = int(get_jwt_identity())
    return jsonify(InferenceService.get_user_runs(user_id)), 200







ALLOWED_AUDIO_EXTENSIONS = {"wav", "mp3", "ogg", "flac", "m4a", "webm"}


def allowed_audio(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_AUDIO_EXTENSIONS


@inference_bp.route("/run-voice-qa", methods=["POST"])
@jwt_required()
def run_voice_qa():
    user_id = int(get_jwt_identity())

    if "audio" not in request.files:
        raise ValidationAppError({"audio": ["Audio file is required"]})

    file = request.files["audio"]

    if not file.filename or not allowed_audio(file.filename):
        raise ValidationAppError({"audio": [f"Unsupported format. Allowed: {', '.join(ALLOWED_AUDIO_EXTENSIONS)}"]})

    # Save audio to uploads folder so Celery worker can read it by path
    upload_dir = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(upload_dir, exist_ok=True)

    ext = secure_filename(file.filename).rsplit(".", 1)[1].lower()
    stored_filename = f"audio_{uuid.uuid4().hex}.{ext}"
    audio_path = os.path.join(upload_dir, stored_filename)
    file.save(audio_path)

    run = InferenceService.create_pending_run(
        user_id=user_id,
        task_name="voice_qa",
        input_data={"audio_path": audio_path},
    )

    task = run_inference_task.delay(run.id)
    run.celery_task_id = task.id

    from app.extensions import db
    db.session.commit()

    return jsonify(run.to_dict()), 202



ALLOWED_IMAGE_EXTENSIONS = {"jpg", "jpeg", "png", "webp", "bmp"}

def allowed_image(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS


@inference_bp.route("/run-cnn", methods=["POST"])
@jwt_required()
def run_cnn():
    user_id = int(get_jwt_identity())

    if "image" not in request.files:
        raise ValidationAppError({"image": ["Image file is required"]})

    file = request.files["image"]

    if not file.filename or not allowed_image(file.filename):
        raise ValidationAppError({"image": [f"Unsupported format. Allowed: {', '.join(ALLOWED_IMAGE_EXTENSIONS)}"]})

    upload_dir = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(upload_dir, exist_ok=True)

    ext = secure_filename(file.filename).rsplit(".", 1)[1].lower()
    stored_filename = f"img_{uuid.uuid4().hex}.{ext}"
    image_path = os.path.join(upload_dir, stored_filename)
    file.save(image_path)

    run = InferenceService.create_pending_run(
        user_id=user_id,
        task_name="cnn_gender",
        input_data={"image_path": image_path},
    )

    task = run_inference_task.delay(run.id)
    run.celery_task_id = task.id

    from app.extensions import db
    db.session.commit()

    return jsonify(run.to_dict()), 202