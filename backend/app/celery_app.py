# backend/app/celery_app.py

from celery import Celery

celery = Celery(__name__)


def init_celery(app):
    """
    Binds Celery to the Flask app's config and wraps every task
    so it executes inside Flask's app context automatically.
    Without this, db.session and current_app would crash inside tasks.
    """
    celery.conf.update(
        broker_url=app.config["CELERY_BROKER_URL"],
        result_backend=app.config["CELERY_RESULT_BACKEND"],
        task_serializer="json",
        result_serializer="json",
        accept_content=["json"],
        timezone="UTC",
        enable_utc=True,
    )

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery