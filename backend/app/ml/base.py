# backend/app/ml/base.py

from abc import ABC, abstractmethod
from typing import Any, Optional
from app.ml.categories import AlgorithmCategory


class BaseAlgorithm(ABC):
    """
    Strategy Pattern interface — every algorithm implements this.
    The rest of the app depends on THIS contract, never on a
    concrete algorithm class. That's what makes algorithms swappable.
    """

    name: str = ""              # registry key, e.g. "naive_bayes"
    display_name: str = ""      # UI label, e.g. "Naive Bayes"
    task_type: str = ""         # "classification" | "regression" | "clustering"
    category: str = AlgorithmCategory.MACHINE_LEARNING
    description: str = ""

    def __init__(self, **params: Any):
        self.params = params
        self.model = None

    @abstractmethod
    def build_model(self):
        """Return a configured sklearn estimator. Each subclass implements this."""
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def get_param_schema(cls) -> list:
        """Return list[ParamDef] describing this algorithm's hyperparameters."""
        raise NotImplementedError

    def fit(self, X_train, y_train: Optional[Any] = None) -> "BaseAlgorithm":
        self.model = self.build_model()
        if y_train is not None:
            self.model.fit(X_train, y_train)
        else:
            self.model.fit(X_train)   # clustering algorithms have no labels
        return self

    def predict(self, X):
        if self.model is None:
            raise RuntimeError("Model not fitted yet. Call fit() first.")
        return self.model.predict(X)