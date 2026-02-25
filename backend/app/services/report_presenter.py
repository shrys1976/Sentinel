def build_report_view(report_json: dict, score: int, dataset) -> dict:
    payload = report_json if isinstance(report_json, dict) else {}
    summary = payload.get("summary", {}) if isinstance(payload.get("summary", {}), dict) else {}

    return {
        "dataset": {
            "id": dataset.id,
            "name": dataset.name,
            "rows": dataset.rows,
            "columns": dataset.columns,
            "created_at": str(dataset.created_at) if getattr(dataset, "created_at", None) else None,
            "status": getattr(dataset, "status", None),
        },
        "sentinel_score": score,
        "top_issues": summary.get("top_issues", []),
        "warnings": summary.get("warnings", []),
        "failed_analyzers": summary.get("failed_analyzers", []),
        "sections": {
            "basic_stats": payload.get("basic_stats", {}),
            "missing": payload.get("missing", {}),
            "imbalance": payload.get("imbalance", {}),
            "leakage": payload.get("leakage", {}),
            "outliers": payload.get("outliers", {}),
            "categorical": payload.get("categorical", {}),
        },
    }
