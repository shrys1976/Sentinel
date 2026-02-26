from __future__ import annotations


def build_recommendations(report: dict) -> dict:
    actions: list[str] = []

    missing = report.get("missing", {}) if isinstance(report.get("missing", {}), dict) else {}
    high_missing = missing.get("high_missing_columns", []) if isinstance(missing.get("high_missing_columns", []), list) else []
    if high_missing:
        actions.append(
            f"Impute or drop high-missing columns: {', '.join(high_missing[:5])}."
        )

    imbalance = report.get("imbalance", {}) if isinstance(report.get("imbalance", {}), dict) else {}
    if imbalance.get("imbalance_detected"):
        actions.append("Mitigate class imbalance using class_weight, focal loss, or SMOTE.")

    structural = report.get("structural_risk", {}) if isinstance(report.get("structural_risk", {}), dict) else {}
    id_columns = structural.get("id_columns", []) if isinstance(structural.get("id_columns", []), list) else []
    if id_columns:
        actions.append("Remove identifier-like columns from model features to reduce memorization risk.")

    target_diag = report.get("target_diagnostics", {}) if isinstance(report.get("target_diagnostics", {}), dict) else {}
    if target_diag.get("weak_signal_detected"):
        actions.append("Engineer higher-signal features or enrich data sources; current target signal is weak.")

    simulation = report.get("model_simulation", {}) if isinstance(report.get("model_simulation", {}), dict) else {}
    if simulation.get("high_overfitting_risk"):
        actions.append("Reduce model complexity and validate with stronger cross-validation to control overfitting.")

    leakage = report.get("leakage", {}) if isinstance(report.get("leakage", {}), dict) else {}
    if leakage.get("leakage_detected"):
        actions.append("Audit suspicious high-correlation features for leakage and exclude leakage-prone columns.")

    if not actions:
        actions.append("No major blockers detected; proceed with baseline model and monitor drift/quality.")

    return {
        "top_actions": actions[:5],
        "total_actions_generated": len(actions),
    }
