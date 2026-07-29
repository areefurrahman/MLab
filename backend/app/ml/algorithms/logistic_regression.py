from sklearn.linear_model import LogisticRegression
from app.ml.base import BaseAlgorithm
from app.ml.registry import AlgorithmRegistry
from app.ml.param_schema import ParamDef


@AlgorithmRegistry.register("logistic_regression")
class LogisticRegressionAlgorithm(BaseAlgorithm):
    name = "logistic_regression"
    display_name = "Logistic Regression"
    task_type = "classification"
    description = "Linear model that estimates class probabilities using the logistic function."

    def build_model(self):
        return LogisticRegression(
            C=self.params.get("C", 1.0),
            max_iter=self.params.get("max_iter", 200),
        )

    @classmethod
    def get_param_schema(cls):
        return [
            ParamDef(name="C", label="Regularization Strength (C)", type="float",
                      default=1.0, min=0.01, max=10.0, step=0.01,
                      description="Lower values mean stronger regularization."),
            ParamDef(name="max_iter", label="Max Iterations", type="int",
                      default=200, min=50, max=1000, step=50),
        ]