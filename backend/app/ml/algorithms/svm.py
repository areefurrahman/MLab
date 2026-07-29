from sklearn.svm import SVC
from app.ml.base import BaseAlgorithm
from app.ml.registry import AlgorithmRegistry
from app.ml.param_schema import ParamDef


@AlgorithmRegistry.register("svm")
class SVMAlgorithm(BaseAlgorithm):
    name = "svm"
    display_name = "Support Vector Machine"
    task_type = "classification"
    description = "Finds the optimal hyperplane that separates classes with maximum margin."

    def build_model(self):
        return SVC(
            C=self.params.get("C", 1.0),
            kernel=self.params.get("kernel", "rbf"),
        )

    @classmethod
    def get_param_schema(cls):
        return [
            ParamDef(name="C", label="Regularization (C)", type="float",
                      default=1.0, min=0.01, max=10.0, step=0.01),
            ParamDef(name="kernel", label="Kernel", type="select",
                      default="rbf", options=["linear", "rbf", "poly"]),
        ]