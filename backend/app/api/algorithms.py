# backend/app/api/algorithms.py

from flask import Blueprint, jsonify
from app.ml.registry import AlgorithmRegistry

algorithms_bp = Blueprint("algorithms", __name__)


@algorithms_bp.route("", methods=["GET"])
def list_algorithms():
    return jsonify(AlgorithmRegistry.list_metadata()), 200


@algorithms_bp.route("/<string:algorithm_name>", methods=["GET"])
def get_algorithm(algorithm_name):
    algo_cls = AlgorithmRegistry.get(algorithm_name)
    return jsonify({
        "name": algo_cls.name,
        "display_name": algo_cls.display_name,
        "task_type": algo_cls.task_type,
        "description": algo_cls.description,
        "parameters": [p.to_dict() for p in algo_cls.get_param_schema()],
    }), 200