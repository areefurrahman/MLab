# backend/app/ml/inference_base.py

from abc import ABC, abstractmethod
from typing import Any


class BaseInferenceTask(ABC):
    """
    Strategy interface for pretrained transformer pipeline tasks.
    Contract: run(input_data) -> output_data.
    No fit(), no train/test split, no metrics dict — deliberately different
    from BaseAlgorithm because the domain is genuinely different.
    """
    name: str = ""
    display_name: str = ""
    category: str = ""
    description: str = ""

    # ─── Model Cache ─────────────────────────────────────────────────────────
    # Class-level attribute. None until first request in this Celery worker
    # process, then stays warm. Re-loads only if the worker restarts.
    # This is what prevents a 5-second model load on every single request.
    _pipeline = None

    @classmethod
    def get_pipeline(cls):
        if cls._pipeline is None:
            cls._pipeline = cls._load_pipeline()
        return cls._pipeline

    @classmethod
    @abstractmethod
    def _load_pipeline(cls):
        """Load and return the HuggingFace pipeline. Called exactly once per worker."""
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def get_input_schema(cls) -> list:
        """Return list[InferenceInputDef] describing what the user submits."""
        raise NotImplementedError

    @abstractmethod
    def run(self, input_data: dict) -> dict:
        """Execute inference. input_data keys match InferenceInputDef names."""
        raise NotImplementedError

    def __init__(self):
        pass