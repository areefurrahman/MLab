from app.celery_app import celery
from app.services.inference_service import InferenceService


@celery.task(bind=True, name="run_inference_task")
def run_inference_task(self, run_id: int):
    return InferenceService.execute_run(run_id)