# backend/app/tasks/experiment_tasks.py

from app.celery_app import celery
from app.services.experiment_service import ExperimentService


@celery.task(bind=True, name="run_experiment_task")
def run_experiment_task(self, experiment_id: int):
    """
    Runs inside the Celery worker process, not the Flask request thread.
    ContextTask (from celery_app.py) wraps this in app_context() automatically,
    so db.session and current_app work normally here.
    """
    return ExperimentService.execute_experiment(experiment_id)