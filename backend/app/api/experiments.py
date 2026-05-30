from flask import Blueprint

experiments_bp = Blueprint("experiments", __name__)

@experiments_bp.route("/ping")
def ping():
    return {"message": "experiments blueprint working"}, 200