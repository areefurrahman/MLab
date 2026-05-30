from flask import Blueprint

algorithms_bp = Blueprint("algorithms", __name__)

@algorithms_bp.route("/ping")
def ping():
    return {"message": "algorithms blueprint working"}, 200