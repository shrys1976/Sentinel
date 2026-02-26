from __future__ import annotations


def compute_score_v2(report: dict) -> tuple[int, dict]:
    score = 100
    penalties: list[dict] = []
    critical_issues: list[str] = []
    warnings: list[str] = []

    def apply(reason: str, amount: int, severity: str = "warning") -> None:
        nonlocal score
        score -= amount
        penalties.append({"reason": reason, "amount": amount})
        if severity == "critical":
            critical_issues.append(reason)
        else:
            warnings.append(reason)

    leakage = report.get("leakage", {}) if isinstance(report.get("leakage", {}), dict) else {}
    if leakage.get("leakage_detected"):
        apply("Potential leakage detected", 50, severity="critical")

    simulation = report.get("model_simulation", {}) if isinstance(report.get("model_simulation", {}), dict) else {}
    baseline_score = simulation.get("baseline_score")
    task_type = simulation.get("task_type")
    if isinstance(baseline_score, (int, float)):
        if task_type == "classification" and baseline_score < 0.6:
            apply("Low baseline AUC indicates weak learnability", 25, severity="critical")
        if task_type == "regression" and baseline_score < 0.2:
            apply("Low baseline R2 indicates weak learnability", 25, severity="critical")
    if simulation.get("high_overfitting_risk"):
        apply("High overfitting risk", 20)

    imbalance = report.get("imbalance", {}) if isinstance(report.get("imbalance", {}), dict) else {}
    if imbalance.get("imbalance_detected"):
        apply("Severe class imbalance", 20)

    missing = report.get("missing", {}) if isinstance(report.get("missing", {}), dict) else {}
    high_missing = missing.get("high_missing_columns", []) if isinstance(missing.get("high_missing_columns", []), list) else []
    if high_missing:
        apply("High missing columns", min(len(high_missing) * 2, 20))

    structural = report.get("structural_risk", {}) if isinstance(report.get("structural_risk", {}), dict) else {}
    if (structural.get("duplicate_ratio") or 0) >= 0.1:
        apply("High duplicate row ratio", 20)
    if structural.get("id_columns"):
        apply("ID-like columns detected", 10)
    if structural.get("timestamp_leakage_candidates"):
        apply("Potential timestamp leakage", 10)

    outliers = report.get("outliers", {}) if isinstance(report.get("outliers", {}), dict) else {}
    high_outlier_columns = outliers.get("high_outlier_columns", []) if isinstance(outliers.get("high_outlier_columns", []), list) else []
    if high_outlier_columns:
        apply("Outlier-dominated columns detected", 10)

    target_diag = report.get("target_diagnostics", {}) if isinstance(report.get("target_diagnostics", {}), dict) else {}
    if target_diag.get("weak_signal_detected"):
        apply("Weak feature-target signal", 30, severity="critical")

    score = max(0, int(score))
    if score >= 80:
        difficulty = "easy"
        modeling_risk = "low"
    elif score >= 55:
        difficulty = "moderate"
        modeling_risk = "medium"
    else:
        difficulty = "difficult"
        modeling_risk = "high"

    return score, {
        "penalties": penalties,
        "critical_issues": critical_issues,
        "warnings": warnings,
        "dataset_difficulty": difficulty,
        "modeling_risk": modeling_risk,
    }
