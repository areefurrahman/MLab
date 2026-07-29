from flask import Flask

from app.utils.error_handlers import register_error_handlers
from .config import config_map
from .extensions import db, migrate, jwt, cors
from .celery_app import init_celery

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

    register_error_handlers(app)
    
    init_celery(app)

    with app.app_context():
        from app.models import User, Dataset, Experiment, ComparisonGroup   
        from app.ml import algorithms # noqa: F401 — registers algorithms
        from app.ml import datasets as _ds     # noqa: F401 — registers built-in datasets
        from app.ml import inference_tasks      # noqa: F401 — registers inference tasks

    # 3. Register Blueprints (routes)
    from .api.auth import auth_bp
    from .api.algorithms import algorithms_bp
    from .api.experiments import experiments_bp
    from .api.datasets import datasets_bp
    from .api.comparisons import comparisons_bp
    from .api.inference import inference_bp
    from .api.history import history_bp

    app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")
    app.register_blueprint(algorithms_bp, url_prefix="/api/v1/algorithms")
    app.register_blueprint(experiments_bp, url_prefix="/api/v1/experiments")
    app.register_blueprint(datasets_bp, url_prefix="/api/v1/datasets")
    app.register_blueprint(comparisons_bp, url_prefix="/api/v1/comparisons")
    app.register_blueprint(inference_bp, url_prefix="/api/v1/inference")
    app.register_blueprint(history_bp, url_prefix="/api/v1/history")

    # 4. Health check route
    @app.route("/api/health")
    def health():
        return {"status": "ok", "message": "MLab API is running"}, 200

    return app