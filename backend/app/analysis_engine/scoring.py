SCORING_RULES = {

    "fully_null_column": 10,
    "high_missing_column": 2,
    "imbalance": 15,
    "leakage": 40,
    "outliers": 10,
    "high_cardinality": 10,
    "duplicate_rows": 10,
}

def compute_score(report: dict):

    score = 100
    critical_issues = []
    warnings = []
    # ---------- BASIC STATS ----------

    basic = report.get("basic_stats", {})

    duplicate_ratio = basic.get(

        "duplicate_ratio",

        0

    )


    if duplicate_ratio >= 0.1:

        score -= SCORING_RULES["duplicate_rows"]

        warnings.append(

            "High duplicate rows detected"

        )


    constant_columns = basic.get(

        "constant_columns",

        []

    )


    if constant_columns:

        penalty = min(

            len(constant_columns),

            5

        )


        score -= penalty

        warnings.append(

            "Constant columns present"

        )


    # ---------- MISSING ----------

    missing = report.get("missing", {})


    fully_null = missing.get(

        "fully_null_columns",

        []

    )


    if fully_null:

        score -= (

            SCORING_RULES["fully_null_column"]

            * len(fully_null)

        )


        critical_issues.append(
            "Fully null columns detected"

        )


    high_missing = missing.get(
        "high_missing_columns",

        []

    )


    score -= (

        SCORING_RULES["high_missing_column"]
        * len(high_missing)

    )


    if high_missing:

        warnings.append(
            "High missing columns detected"

        )


    # ---------- IMBALANCE ----------

    imbalance = report.get(
        "imbalance",

        {}
    )

    if imbalance.get(
        "imbalance_detected"

    ):

        score -= SCORING_RULES["imbalance"]
        warnings.append(
            "Severe class imbalance"

        )


    # ---------- LEAKAGE ----------

    leakage = report.get(

        "leakage",
        {}

    )


    if leakage.get(
        "leakage_detected"

    ):

        score -= SCORING_RULES["leakage"]
        critical_issues.append(
            "Potential feature leakage"

        )


    # ---------- OUTLIERS ----------

    outliers = report.get(
        "outliers",
        {}

    )


    high_outlier_columns = outliers.get(
        "high_outlier_columns",
        []

    )


    if high_outlier_columns:

        score -= SCORING_RULES["outliers"]
        warnings.append(
            "High outlier presence"

        )


    # ---------- CATEGORICAL ----------

    categorical = report.get(
        "categorical",
        {}

    )


    high_cardinality = categorical.get(
        "high_cardinality_columns",
        []

    )


    if high_cardinality:

        score -= SCORING_RULES["high_cardinality"]
        warnings.append(
            "High cardinality categorical columns"

        )


    score = max(score, 0)

    summary = {
        "critical_issues":
            critical_issues,
        "warnings":
            warnings,

    }

    return score, summary