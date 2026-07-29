# backend/app/ml/preprocessing.py

import pandas as pd
from sklearn.preprocessing import LabelEncoder
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from mlxtend.preprocessing import TransactionEncoder
from app.utils.exceptions import ValidationAppError

def prepare_features_and_target(df: pd.DataFrame, target_column: str):
    """
    Intentionally basic: drop missing rows, label-encode categoricals.
    A real pipeline would do much more — but explicit and predictable
    beats clever and invisible for a learning tool.
    """
    df = df.dropna()

    y_raw = df[target_column]
    X_df = df.drop(columns=[target_column])

    for col in X_df.columns:
        if X_df[col].dtype == object:
            X_df[col] = LabelEncoder().fit_transform(X_df[col])

    target_names = None
    if y_raw.dtype == object or y_raw.dtype.name == "str" or y_raw.dtype.kind in ("O", "U"):
        encoder = LabelEncoder()
        y = encoder.fit_transform(y_raw)
        target_names = list(encoder.classes_)
    else:
        y = y_raw.values

    return X_df.values, y, list(X_df.columns), target_names


def parse_transaction_column(df: pd.DataFrame, items_column: str) -> list:
    """Parses a CSV column of comma-separated items into list-of-lists."""
    if items_column not in df.columns:
        raise ValidationAppError({"items_column": ["Column not found in dataset"]})

    transactions = (
        df[items_column].dropna().astype(str)
        .apply(lambda row: [item.strip() for item in row.split(",") if item.strip()])
        .tolist()
    )
    if len(transactions) == 0:
        raise ValidationAppError({"items_column": ["No valid transactions found"]})
    return transactions


def encode_transactions(transactions: list) -> pd.DataFrame:
    """list-of-lists → one-hot boolean DataFrame (columns=items, rows=transactions)."""
    encoder = TransactionEncoder()
    encoded_array = encoder.fit(transactions).transform(transactions)
    return pd.DataFrame(encoded_array, columns=encoder.columns_)