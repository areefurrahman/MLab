from sklearn.tree import DecisionTreeClassifier
from app.ml.base import BaseAlgorithm
from app.ml.registry import AlgorithmRegistry
from app.ml.param_schema import ParamDef


@AlgorithmRegistry.register("decision_tree")
class DecisionTreeAlgorithm(BaseAlgorithm):
    name = "decision_tree"
    display_name = "Decision Tree"
    task_type = "classification"
    description = "Splits data into branches based on feature thresholds to reach a decision."

    def build_model(self):
        return DecisionTreeClassifier(
            max_depth=self.params.get("max_depth", 5),
            criterion=self.params.get("criterion", "gini"),
        )

    @classmethod
    def get_param_schema(cls):
        return [
            ParamDef(name="max_depth", label="Max Depth", type="int",
                      default=5, min=1, max=20, step=1),
            ParamDef(name="criterion", label="Split Criterion", type="select",
                      default="gini", options=["gini", "entropy"]),
        ]