# backend/app/utils/json_utils.py

import numpy as np


def to_json_safe(value):
    """
    Recursively converts numpy types into native Python types.
    Without this, every sklearn metric (accuracy, confusion_matrix, etc.)
    crashes jsonify() and JSON DB columns.
    """
    if isinstance(value, dict):
        return {k: to_json_safe(v) for k, v in value.items()}

    if isinstance(value, (list, tuple)):
        return [to_json_safe(v) for v in value]

    if isinstance(value, np.ndarray):
        return to_json_safe(value.tolist())

    if isinstance(value, np.integer):
        return int(value)

    if isinstance(value, np.floating):
        return float(value)

    if isinstance(value, np.bool_):
        return bool(value)

    return value