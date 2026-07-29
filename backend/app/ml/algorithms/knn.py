# backend/app/ml/algorithms/knn.py

from sklearn.neighbors import KNeighborsClassifier
from app.ml.base import BaseAlgorithm
from app.ml.registry import AlgorithmRegistry
from app.ml.param_schema import ParamDef


@AlgorithmRegistry.register("knn")
class KNNAlgorithm(BaseAlgorithm):
    name = "knn"
    display_name = "K-Nearest Neighbors"
    task_type = "classification"
    description = "Classifies a point based on the majority class among its K nearest neighbors."

    def build_model(self):
        return KNeighborsClassifier(
            n_neighbors=self.params.get("n_neighbors", 5),
            weights=self.params.get("weights", "uniform"),
        )

    @classmethod
    def get_param_schema(cls):
        return [
            ParamDef(name="n_neighbors", label="Number of Neighbors (K)", type="int",
                      default=5, min=1, max=20, step=1),
            ParamDef(name="weights", label="Weight Function", type="select",
                      default="uniform", options=["uniform", "distance"]),
        ]