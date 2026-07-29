from sklearn.cluster import KMeans
from app.ml.base import BaseAlgorithm
from app.ml.registry import AlgorithmRegistry
from app.ml.param_schema import ParamDef


@AlgorithmRegistry.register("kmeans")
class KMeansAlgorithm(BaseAlgorithm):
    name = "kmeans"
    display_name = "K-Means Clustering"
    task_type = "clustering"
    description = "Groups data into K clusters by minimizing distance to cluster centroids."

    def build_model(self):
        return KMeans(
            n_clusters=self.params.get("n_clusters", 3),
            n_init=10,
            random_state=42,
        )

    @classmethod
    def get_param_schema(cls):
        return [
            ParamDef(name="n_clusters", label="Number of Clusters (K)", type="int",
                      default=3, min=2, max=10, step=1),
        ]