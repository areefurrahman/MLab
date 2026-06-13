from flask import Flask
from .config import config_map
from .extensions import db, migrate, jwt, cors

def create_app(config_name: str = "development") -> Flask:
   
   
    """
    App Factory — creates and configures the Flask app.
    Called once at startup (or per test with different config).
    """


    app = Flask(__name__)


    # 1. Load config
    app.config.from_object(config_map[config_name])

    # 2. Initialize extensions (attach them to THIS app instance)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})


    with app.app_context():
        from app.models import User, Dataset, Experiment

    # 3. Register Blueprints (routes)
    from .api.auth import auth_bp
    from .api.algorithms import algorithms_bp
    from .api.experiments import experiments_bp

    app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")
    app.register_blueprint(algorithms_bp, url_prefix="/api/v1/algorithms")
    app.register_blueprint(experiments_bp, url_prefix="/api/v1/experiments")

    # 4. Health check route
    @app.route("/api/health")
    def health():
        return {"status": "ok", "message": "MLab API is running"}, 200

    return app