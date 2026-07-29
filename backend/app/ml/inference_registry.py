# backend/app/ml/inference_registry.py

from app.utils.exceptions import NotFoundError


class InferenceTaskRegistry:
    """
    Same Registry+decorator pattern as AlgorithmRegistry.
    Maps task name strings to BaseInferenceTask subclasses.
    """
    _registry: dict = {}

    @classmethod
    def register(cls, key: str):
        def decorator(task_class):
            cls._registry[key] = task_class
            return task_class
        return decorator

    @classmethod
    def get(cls, key: str):
        if key not in cls._registry:
            raise NotFoundError(f"Inference task '{key}' not found")
        return cls._registry[key]

    @classmethod
    def get_all(cls) -> dict:
        return cls._registry

    @classmethod
    def list_metadata(cls) -> list:
        return [
            {
                "name": key,
                "display_name": task_cls.display_name,
                "category": task_cls.category,
                "description": task_cls.description,
                "input_schema": [f.to_dict() for f in task_cls.get_input_schema()],
            }
            for key, task_cls in cls._registry.items()
        ]