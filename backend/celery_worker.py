# backend/celery_worker.py

import os
from app import create_app
from app.celery_app import celery

config_name = os.getenv("FLASK_ENV", "development")
flask_app = create_app(config_name)
flask_app.app_context().push()