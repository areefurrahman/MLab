# backend/app/ml/registry.py

from app.utils.exceptions import NotFoundError
from app.ml.categories import AlgorithmCategory


class AlgorithmRegistry:
    """
    Self-populating registry. Algorithms register themselves via decorator —
    nobody maintains a master list by hand. Add a file, add one decorator,
    the system discovers it automatically.
    """

    _registry: dict = {}

    @classmethod
    def register(cls, key: str):
        def decorator(algorithm_class):
            cls._registry[key] = algorithm_class
            return algorithm_class
        return decorator

    @classmethod
    def get(cls, key: str):
        if key not in cls._registry:
            raise NotFoundError(f"Algorithm '{key}' not found")
        return cls._registry[key]

    @classmethod
    def get_all(cls) -> dict:
        return cls._registry

    @classmethod
    def list_metadata(cls) -> list:
        return [
            {
                "name": key,
                "display_name": algo_cls.display_name,
                "task_type": algo_cls.task_type,
                "category": algo_cls.category,
                "category_label": AlgorithmCategory.LABELS.get(algo_cls.category, algo_cls.category),
                "description": algo_cls.description,
                "parameters": [p.to_dict() for p in algo_cls.get_param_schema()],
            }
            for key, algo_cls in cls._registry.items()
        ]