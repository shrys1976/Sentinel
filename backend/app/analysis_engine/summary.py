def build_summary(
    report: dict,
    score: int,
    scoring_summary : dict
):

 critical =  scoring_summary.get("critical_issues", [])
 warnings = scoring_summary.get("warnings", [])

 summary = {

    "sentinel_score": score,
    "top_issues" : critical[:5],
    "warnings": warnings[:5],
    "failed_analyzers" : report.get("failed_analyzers",[]),

 }

 return summary

 