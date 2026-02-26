def build_summary(
    report: dict,
    score: int,
    scoring_summary: dict
):

 critical = scoring_summary.get("critical_issues", [])
 warnings = scoring_summary.get("warnings", [])
 ingestion = report.get("ingestion", {}) if isinstance(report.get("ingestion", {}), dict) else {}
 ingestion_warnings = ingestion.get("warnings", []) if isinstance(ingestion.get("warnings", []), list) else []

 summary = {

    "sentinel_score": score,
    "top_issues" : critical[:5],
    "warnings": (warnings + ingestion_warnings)[:5],
    "failed_analyzers" : report.get("failed_analyzers",[]),

 }

 return summary

 
