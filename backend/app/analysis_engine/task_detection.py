from __future__ import annotations

import pandas as pd


def detect_task_type(target: pd.Series) -> str:
    non_null = target.dropna()
    if non_null.empty:
        return "unknown"

    if pd.api.types.is_numeric_dtype(non_null):
        unique_count = int(non_null.nunique())
        unique_ratio = float(unique_count) / float(len(non_null))
        if unique_count <= 20 and unique_ratio <= 0.05:
            return "classification"
        return "regression"

    return "classification"
