from __future__ import annotations

from typing import Any

import pandas as pd


ID_NAME_HINTS = ("id", "uuid", "email", "account", "customer")


def _is_datetime_like(series: pd.Series) -> bool:
    if pd.api.types.is_datetime64_any_dtype(series):
        return True
    sample = series.dropna().astype("string").head(100)
    if sample.empty:
        return False
    parsed = pd.to_datetime(sample, errors="coerce", utc=True)
    return parsed.notna().mean() >= 0.8


def run_structural_risk_analysis(
    df: pd.DataFrame,
    target_column: str | None,
) -> dict[str, Any]:
    rows = len(df)
    if rows == 0:
        return {"skipped": True, "reason": "empty_dataframe"}

    id_columns: list[dict[str, Any]] = []
    repeated_entity_identifiers: list[dict[str, Any]] = []
    timestamp_leakage_candidates: list[dict[str, Any]] = []

    duplicate_rows = int(df.duplicated().sum())
    duplicate_ratio = round(float(duplicate_rows / rows), 4)

    for col in df.columns:
        series = df[col]
        non_null = series.dropna()
        if non_null.empty:
            continue

        uniqueness_ratio = float(non_null.nunique()) / float(len(non_null))
        lower_name = col.lower()
        is_hint = any(hint in lower_name for hint in ID_NAME_HINTS)
        if uniqueness_ratio >= 0.98 or is_hint:
            id_columns.append(
                {
                    "column": col,
                    "uniqueness_ratio": round(float(uniqueness_ratio), 4),
                    "name_hint": is_hint,
                }
            )
            duplicate_entity_count = int(non_null.duplicated().sum())
            if duplicate_entity_count > 0:
                repeated_entity_identifiers.append(
                    {
                        "column": col,
                        "duplicate_identifier_rows": duplicate_entity_count,
                    }
                )

        if col == target_column:
            continue

        if _is_datetime_like(series):
            parsed = pd.to_datetime(series, errors="coerce", utc=True)
            parsed_non_null = parsed.dropna()
            if parsed_non_null.empty:
                continue

            monotonic = bool(parsed_non_null.is_monotonic_increasing or parsed_non_null.is_monotonic_decreasing)
            signal = {
                "column": col,
                "monotonic": monotonic,
            }
            timestamp_leakage_candidates.append(signal)

    return {
        "duplicate_rows": duplicate_rows,
        "duplicate_ratio": duplicate_ratio,
        "id_columns": id_columns,
        "repeated_entity_identifiers": repeated_entity_identifiers,
        "timestamp_leakage_candidates": timestamp_leakage_candidates,
        "high_structural_risk": duplicate_ratio >= 0.1
        or bool(id_columns)
        or any(item.get("monotonic") for item in timestamp_leakage_candidates),
    }
