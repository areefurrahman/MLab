from sklearn.naive_bayes import GaussianNB
from app.ml.base import BaseAlgorithm
from app.ml.registry import AlgorithmRegistry
from app.ml.param_schema import ParamDef


@AlgorithmRegistry.register("naive_bayes")
class NaiveBayesAlgorithm(BaseAlgorithm):
    name = "naive_bayes"
    display_name = "Naive Bayes"
    task_type = "classification"
    description = "Probabilistic classifier based on Bayes' theorem, assuming feature independence."

    def build_model(self):
        return GaussianNB(var_smoothing=self.params.get("var_smoothing", 1e-9))

    @classmethod
    def get_param_schema(cls):
        return [
            ParamDef(
                name="var_smoothing", label="Variance Smoothing", type="float",
                default=1e-9, min=1e-12, max=1e-6, step=1e-9,
                description="Stability term added to variance calculations."
            )
        ]