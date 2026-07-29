# backend/app/ml/metrics.py

from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, silhouette_score,
)
from app.utils.json_utils import to_json_safe


def compute_classification_metrics(y_test, y_pred) -> dict:
    return to_json_safe({
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred, average="weighted", zero_division=0),
        "recall": recall_score(y_test, y_pred, average="weighted", zero_division=0),
        "f1_score": f1_score(y_test, y_pred, average="weighted", zero_division=0),
        "confusion_matrix": confusion_matrix(y_test, y_pred),
    })


def compute_clustering_metrics(X, labels) -> dict:
    metrics = {"n_clusters_found": len(set(labels))}
    if len(set(labels)) > 1:
        metrics["silhouette_score"] = silhouette_score(X, labels)
    return to_json_safe(metrics)