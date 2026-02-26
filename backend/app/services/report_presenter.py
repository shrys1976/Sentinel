def build_report_view(
    report_json: dict,
    score: int,
    dataset,
    available_plots: list[str] | None = None,
) -> dict:
    payload = report_json if isinstance(report_json, dict) else {}
    summary = payload.get("summary", {}) if isinstance(payload.get("summary", {}), dict) else {}
    scores = payload.get("scores", {}) if isinstance(payload.get("scores", {}), dict) else {}
    score_v2_meta = scores.get("v2_meta", {}) if isinstance(scores.get("v2_meta", {}), dict) else {}

    return {
        "dataset": {
            "id": dataset.id,
            "name": dataset.name,
            "rows": dataset.rows,
            "columns": dataset.columns,
            "created_at": str(dataset.created_at) if getattr(dataset, "created_at", None) else None,
            "status": getattr(dataset, "status", None),
            "target_column": getattr(dataset, "target_column", None),
        },
        "sentinel_score": score,
        "dataset_difficulty": score_v2_meta.get("dataset_difficulty"),
        "modeling_risk": score_v2_meta.get("modeling_risk"),
        "top_issues": summary.get("top_issues", []),
        "warnings": summary.get("warnings", []),
        "failed_analyzers": summary.get("failed_analyzers", []),
        "recommended_actions": summary.get("recommended_actions", []),
        "available_plots": available_plots or [],
        "sections": {
            "ingestion": payload.get("ingestion", {}),
            "basic_stats": payload.get("basic_stats", {}),
            "missing": payload.get("missing", {}),
            "imbalance": payload.get("imbalance", {}),
            "leakage": payload.get("leakage", {}),
            "outliers": payload.get("outliers", {}),
            "categorical": payload.get("categorical", {}),
            "target_diagnostics": payload.get("target_diagnostics", {}),
            "model_simulation": payload.get("model_simulation", {}),
            "structural_risk": payload.get("structural_risk", {}),
            "recommendations": payload.get("recommendations", {}),
        },
    }
