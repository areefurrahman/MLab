# backend/app/ml/datasets.py

from sklearn.datasets import load_iris, load_wine, load_breast_cancer, make_blobs


class BuiltinDatasetRegistry:
    _registry: dict = {}

    @classmethod
    def register(cls, key: str):
        def decorator(loader_fn):
            cls._registry[key] = loader_fn
            return loader_fn
        return decorator

    @classmethod
    def get(cls, key: str):
        from app.utils.exceptions import NotFoundError
        if key not in cls._registry:
            raise NotFoundError(f"Built-in dataset '{key}' not found")
        return cls._registry[key]

    @classmethod
    def list_metadata(cls) -> list:
        return [fn(metadata_only=True) for fn in cls._registry.values()]


@BuiltinDatasetRegistry.register("iris")
def load_iris_dataset(metadata_only=False):
    meta = {
        "key": "iris", "name": "Iris Flowers", "task_type": "classification",
        "rows": 150, "features": 4,
        "description": "Classic dataset of 3 iris species from 4 measurements.",
    }
    if metadata_only:
        return meta
    data = load_iris()
    return {**meta, "X": data.data, "y": data.target,
            "feature_names": list(data.feature_names),
            "target_names": list(data.target_names)}


@BuiltinDatasetRegistry.register("wine")
def load_wine_dataset(metadata_only=False):
    meta = {
        "key": "wine", "name": "Wine Classification", "task_type": "classification",
        "rows": 178, "features": 13,
        "description": "Chemical analysis of wines from 3 cultivars.",
    }
    if metadata_only:
        return meta
    data = load_wine()
    return {**meta, "X": data.data, "y": data.target,
            "feature_names": list(data.feature_names),
            "target_names": list(data.target_names)}


@BuiltinDatasetRegistry.register("breast_cancer")
def load_breast_cancer_dataset(metadata_only=False):
    meta = {
        "key": "breast_cancer", "name": "Breast Cancer Diagnosis", "task_type": "classification",
        "rows": 569, "features": 30,
        "description": "Diagnostic measurements classifying tumors as malignant/benign.",
    }
    if metadata_only:
        return meta
    data = load_breast_cancer()
    return {**meta, "X": data.data, "y": data.target,
            "feature_names": list(data.feature_names),
            "target_names": list(data.target_names)}


@BuiltinDatasetRegistry.register("blobs")
def load_blobs_dataset(metadata_only=False):
    meta = {
        "key": "blobs", "name": "Synthetic Blobs", "task_type": "clustering",
        "rows": 300, "features": 2,
        "description": "Synthetic 2D clusters — ideal for visualizing K-Means.",
    }
    if metadata_only:
        return meta
    X, y = make_blobs(n_samples=300, centers=4, n_features=2, random_state=42)
    return {**meta, "X": X, "y": y, "feature_names": ["x1", "x2"], "target_names": None}



@BuiltinDatasetRegistry.register("groceries")
def load_groceries_dataset(metadata_only=False):
    meta = {
        "key": "groceries", "name": "Grocery Basket Transactions", "task_type": "association_rules",
        "rows": 20, "features": None,
        "description": "Synthetic grocery store transactions for mining 'if-then' purchase rules.",
    }
    if metadata_only:
        return meta

    transactions = [
        ["milk", "bread", "eggs"], ["bread", "butter"], ["milk", "bread", "butter", "eggs"],
        ["bread", "jam"], ["milk", "bread", "jam"], ["eggs", "bacon"],
        ["bread", "butter", "jam"], ["milk", "eggs", "bacon"], ["bread", "milk"],
        ["butter", "jam", "bread"], ["milk", "bread", "butter"], ["eggs", "bread", "bacon"],
        ["milk", "butter"], ["bread", "eggs"], ["milk", "bread", "eggs", "bacon"],
        ["jam", "bread"], ["milk", "jam"], ["bread", "butter", "eggs"],
        ["bacon", "eggs", "bread"], ["milk", "bread", "butter", "jam"],
    ]
    return {**meta, "transactions": transactions, "feature_names": None, "target_names": None}