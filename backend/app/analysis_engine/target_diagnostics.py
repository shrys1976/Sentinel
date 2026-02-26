from __future__ import annotations

from typing import Any

import pandas as pd

from .task_detection import detect_task_type


def _prepare_features(df: pd.DataFrame, target_column: str) -> pd.DataFrame:
    x = df.drop(columns=[target_column], errors="ignore").copy()
    if x.empty:
        return x

    numeric_cols = x.select_dtypes(include="number").columns.tolist()
    for col in numeric_cols:
        x[col] = x[col].fillna(x[col].median())

    categorical_cols = [col for col in x.columns if col not in numeric_cols]
    for col in categorical_cols:
        x[col] = x[col].astype("string").fillna("__MISSING__")

    return pd.get_dummies(x, columns=categorical_cols, drop_first=False)


def run_target_diagnostics(df: pd.DataFrame, target_column: str | None) -> dict[str, Any]:
    if not target_column:
        return {"skipped": True, "reason": "no_target_column"}
    if target_column not in df.columns:
        return {"skipped": True, "reason": "target_column_not_found"}

    y_raw = df[target_column]
    task_type = detect_task_type(y_raw)
    if task_type == "unknown":
        return {"skipped": True, "reason": "empty_target"}

    mask = ~y_raw.isna()
    x_encoded = _prepare_features(df.loc[mask], target_column)
    y = y_raw.loc[mask]

    if x_encoded.empty or y.empty:
        return {"skipped": True, "reason": "insufficient_features"}

    feature_signal_strength: dict[str, float] = {}
    low_signal_features: list[str] = []
    signal_metric = "mi"

    try:
        from sklearn.feature_selection import f_regression, mutual_info_classif

        if task_type == "classification":
            y_for_mi = pd.factorize(y.astype("string"))[0]
            mi_scores = mutual_info_classif(
                x_encoded,
                y_for_mi,
                discrete_features="auto",
                random_state=42,
            )
            feature_signal_strength = {
                col: round(float(score), 4) for col, score in zip(x_encoded.columns, mi_scores)
            }
            low_signal_features = [
                col for col, score in feature_signal_strength.items() if score < 0.005
            ][:20]
        else:
            signal_metric = "f_score"
            y_num = pd.to_numeric(y, errors="coerce")
            valid = ~y_num.isna()
            x_valid = x_encoded.loc[valid]
            y_valid = y_num.loc[valid]
            if x_valid.empty or y_valid.empty:
                return {"skipped": True, "reason": "target_not_numeric_for_regression"}
            f_scores, _ = f_regression(x_valid, y_valid)
            feature_signal_strength = {
                col: round(float(score), 4)
                for col, score in zip(x_valid.columns, f_scores)
                if pd.notna(score)
            }
            low_signal_features = [
                col for col, score in feature_signal_strength.items() if score < 1.0
            ][:20]
    except Exception as exc:
        return {"skipped": True, "reason": f"signal_computation_failed: {exc}"}

    top_predictive_features = [
        {"feature": col, "score": score}
        for col, score in sorted(
            feature_signal_strength.items(),
            key=lambda item: item[1],
            reverse=True,
        )[:10]
    ]

    # Missingness correlated with target.
    target_missing_bias: list[dict[str, Any]] = []
    if task_type == "classification":
        try:
            from scipy.stats import chi2_contingency
        except Exception:
            chi2_contingency = None

        y_cls = y_raw.astype("string")
        for column in df.columns:
            if column == target_column:
                continue
            missing_mask = df[column].isna()
            if not missing_mask.any():
                continue
            contingency = pd.crosstab(missing_mask, y_cls)
            if contingency.shape[0] < 2 or contingency.shape[1] < 2:
                continue
            if chi2_contingency is None:
                break
            chi2, p_value, _, _ = chi2_contingency(contingency.values)
            if p_value < 0.05:
                target_missing_bias.append(
                    {
                        "column": column,
                        "p_value": round(float(p_value), 6),
                        "chi2": round(float(chi2), 4),
                    }
                )

    return {
        "task_type": task_type,
        "target_column": target_column,
        "signal_metric": signal_metric,
        "top_predictive_features": top_predictive_features,
        "low_signal_features": low_signal_features,
        "target_missing_bias": target_missing_bias[:20],
        "weak_signal_detected": len(top_predictive_features) == 0
        or (
            task_type == "classification"
            and top_predictive_features[0]["score"] < 0.02
        )
        or (
            task_type == "regression"
            and top_predictive_features
            and top_predictive_features[0]["score"] < 5.0
        ),
    }
