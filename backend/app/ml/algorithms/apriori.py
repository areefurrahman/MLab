# backend/app/ml/algorithms/apriori.py

import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

from app.ml.base import BaseAlgorithm
from app.ml.registry import AlgorithmRegistry
from app.ml.categories import AlgorithmCategory
from app.ml.param_schema import ParamDef


@AlgorithmRegistry.register("apriori")
class AprioriAlgorithm(BaseAlgorithm):
    name = "apriori"
    display_name = "A-priori (Association Rules)"
    task_type = "association_rules"
    category = AlgorithmCategory.MACHINE_LEARNING
    description = "Mines frequent itemsets and generates if-then purchase rules from transactional data."

    def build_model(self):
        # No sklearn estimator exists for this — fit() is overridden instead.
        return None

    def fit(self, one_hot_df: pd.DataFrame, y=None) -> "AprioriAlgorithm":
        """
        Overrides the base class entirely. Apriori mines the FULL dataset —
        no train/test split applies here.
        """
        min_support = self.params.get("min_support", 0.1)
        min_confidence = self.params.get("min_confidence", 0.5)
        metric = self.params.get("metric", "confidence")

        frequent_itemsets = apriori(one_hot_df, min_support=min_support, use_colnames=True)

        if frequent_itemsets.empty:
            self.rules = pd.DataFrame()
            return self

        rules = association_rules(frequent_itemsets, metric=metric, min_threshold=min_confidence)
        self.rules = rules.sort_values("lift", ascending=False)
        return self

    def predict(self, X=None):
        raise NotImplementedError("Apriori has no predict step — use .rules after fit()")

    @classmethod
    def get_param_schema(cls):
        return [
            ParamDef(name="min_support", label="Minimum Support", type="float",
                      default=0.1, min=0.01, max=1.0, step=0.01,
                      description="How frequently an itemset must appear across all transactions."),
            ParamDef(name="min_confidence", label="Minimum Confidence", type="float",
                      default=0.5, min=0.05, max=1.0, step=0.05,
                      description="How often the rule has held true."),
            ParamDef(name="metric", label="Ranking Metric", type="select",
                      default="confidence", options=["confidence", "lift", "support"]),
        ]