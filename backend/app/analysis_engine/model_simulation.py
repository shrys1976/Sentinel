from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd


MAX_SIMULATION_ROWS = 100_000


def _prepare_xy(df: pd.DataFrame, target_column: str) -> tuple[pd.DataFrame, pd.Series]:
    sample_df = df.copy()
    if len(sample_df) > MAX_SIMULATION_ROWS:
        sample_df = sample_df.sample(n=MAX_SIMULATION_ROWS, random_state=42)

    y = sample_df[target_column]
    x = sample_df.drop(columns=[target_column], errors="ignore")

    numeric_cols = x.select_dtypes(include="number").columns.tolist()
    for col in numeric_cols:
        x[col] = x[col].fillna(x[col].median())

    categorical_cols = [col for col in x.columns if col not in numeric_cols]
    for col in categorical_cols:
        x[col] = x[col].astype("string").fillna("__MISSING__")

    x = pd.get_dummies(x, columns=categorical_cols, drop_first=False)
    return x, y


def run_model_simulation(
    df: pd.DataFrame,
    target_column: str | None,
    task_type: str,
) -> dict[str, Any]:
    try:
        from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
        from sklearn.linear_model import LogisticRegression
        from sklearn.metrics import (
            accuracy_score,
            mean_absolute_error,
            mean_squared_error,
            precision_recall_fscore_support,
            r2_score,
            roc_auc_score,
        )
        from sklearn.model_selection import train_test_split
        from sklearn.preprocessing import LabelEncoder
    except Exception as exc:
        return {"skipped": True, "reason": f"sklearn_unavailable: {exc}"}

    if not target_column:
        return {"skipped": True, "reason": "no_target_column"}
    if target_column not in df.columns:
        return {"skipped": True, "reason": "target_column_not_found"}
    if task_type not in {"classification", "regression"}:
        return {"skipped": True, "reason": "unsupported_task_type"}

    x, y = _prepare_xy(df, target_column)
    mask = ~y.isna()
    x = x.loc[mask]
    y = y.loc[mask]
    if len(x) < 100 or x.empty:
        return {"skipped": True, "reason": "insufficient_rows_after_cleanup"}

    if task_type == "classification":
        y_text = y.astype("string")
        if y_text.nunique() < 2:
            return {"skipped": True, "reason": "target_has_single_class"}
        le = LabelEncoder()
        y_encoded = le.fit_transform(y_text)
        stratify = y_encoded if len(np.unique(y_encoded)) > 1 else None
        x_train, x_val, y_train, y_val = train_test_split(
            x,
            y_encoded,
            test_size=0.2,
            random_state=42,
            stratify=stratify,
        )

        lr = LogisticRegression(max_iter=500, n_jobs=None, class_weight="balanced")
        rf = RandomForestClassifier(
            n_estimators=150,
            max_depth=8,
            random_state=42,
            n_jobs=-1,
            class_weight="balanced_subsample",
        )

        lr.fit(x_train, y_train)
        rf.fit(x_train, y_train)

        lr_pred = lr.predict(x_val)
        rf_pred = rf.predict(x_val)
        lr_train_pred = lr.predict(x_train)
        rf_train_pred = rf.predict(x_train)

        lr_proba = lr.predict_proba(x_val)
        rf_proba = rf.predict_proba(x_val)
        lr_train_proba = lr.predict_proba(x_train)
        rf_train_proba = rf.predict_proba(x_train)

        average = "binary" if len(le.classes_) == 2 else "weighted"
        lr_precision, lr_recall, _, _ = precision_recall_fscore_support(
            y_val,
            lr_pred,
            average=average,
            zero_division=0,
        )
        rf_precision, rf_recall, _, _ = precision_recall_fscore_support(
            y_val,
            rf_pred,
            average=average,
            zero_division=0,
        )

        if len(le.classes_) == 2:
            lr_auc_val = roc_auc_score(y_val, lr_proba[:, 1])
            rf_auc_val = roc_auc_score(y_val, rf_proba[:, 1])
            lr_auc_train = roc_auc_score(y_train, lr_train_proba[:, 1])
            rf_auc_train = roc_auc_score(y_train, rf_train_proba[:, 1])
        else:
            lr_auc_val = roc_auc_score(y_val, lr_proba, multi_class="ovr")
            rf_auc_val = roc_auc_score(y_val, rf_proba, multi_class="ovr")
            lr_auc_train = roc_auc_score(y_train, lr_train_proba, multi_class="ovr")
            rf_auc_train = roc_auc_score(y_train, rf_train_proba, multi_class="ovr")

        models = {
            "logistic_regression": {
                "train_auc": round(float(lr_auc_train), 4),
                "validation_auc": round(float(lr_auc_val), 4),
                "accuracy": round(float(accuracy_score(y_val, lr_pred)), 4),
                "precision": round(float(lr_precision), 4),
                "recall": round(float(lr_recall), 4),
            },
            "random_forest": {
                "train_auc": round(float(rf_auc_train), 4),
                "validation_auc": round(float(rf_auc_val), 4),
                "accuracy": round(float(accuracy_score(y_val, rf_pred)), 4),
                "precision": round(float(rf_precision), 4),
                "recall": round(float(rf_recall), 4),
            },
        }

        best_model_name = max(
            models.keys(),
            key=lambda name: models[name]["validation_auc"],
        )
        best = models[best_model_name]
        overfit_gap = float(best["train_auc"]) - float(best["validation_auc"])
        learnability_score = float(best["validation_auc"])

        return {
            "task_type": "classification",
            "sample_size": int(len(x)),
            "models": models,
            "best_model": best_model_name,
            "baseline_metric": "roc_auc",
            "baseline_score": round(float(learnability_score), 4),
            "overfitting_gap": round(float(overfit_gap), 4),
            "high_overfitting_risk": overfit_gap >= 0.12,
            "weak_learnability": learnability_score < 0.6,
        }

    y_num = pd.to_numeric(y, errors="coerce")
    valid = ~y_num.isna()
    x = x.loc[valid]
    y_num = y_num.loc[valid]
    if len(x) < 100:
        return {"skipped": True, "reason": "insufficient_numeric_target_rows"}

    x_train, x_val, y_train, y_val = train_test_split(
        x,
        y_num,
        test_size=0.2,
        random_state=42,
    )

    rf = RandomForestRegressor(
        n_estimators=150,
        max_depth=10,
        random_state=42,
        n_jobs=-1,
    )
    rf.fit(x_train, y_train)
    val_pred = rf.predict(x_val)
    train_pred = rf.predict(x_train)

    val_r2 = r2_score(y_val, val_pred)
    train_r2 = r2_score(y_train, train_pred)

    return {
        "task_type": "regression",
        "sample_size": int(len(x)),
        "models": {
            "random_forest_regressor": {
                "train_r2": round(float(train_r2), 4),
                "validation_r2": round(float(val_r2), 4),
                "mae": round(float(mean_absolute_error(y_val, val_pred)), 4),
                "rmse": round(float(mean_squared_error(y_val, val_pred, squared=False)), 4),
            }
        },
        "best_model": "random_forest_regressor",
        "baseline_metric": "r2",
        "baseline_score": round(float(val_r2), 4),
        "overfitting_gap": round(float(train_r2 - val_r2), 4),
        "high_overfitting_risk": (train_r2 - val_r2) >= 0.2,
        "weak_learnability": val_r2 < 0.2,
    }
