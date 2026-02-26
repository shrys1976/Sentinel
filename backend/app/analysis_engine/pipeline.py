import logging

from app.analysis_engine.data_loader import load_dataframe
from app.analysis_engine.analyzers.basic_stats import BasicStatsAnalyzer
from app.analysis_engine.analyzers.missing import MissingAnalyzer
from app.analysis_engine.analyzers.imbalance import ImbalanceAnalyzer
from app.analysis_engine.analyzers.leakage import LeakageAnalyzer
from app.analysis_engine.analyzers.outliers import OutlierAnalyzer
from app.analysis_engine.analyzers.categorical import CategoricalAnalyzer
from app.analysis_engine.summary import build_summary
from app.analysis_engine.profile import build_dataset_profile
from app.analysis_engine.target_diagnostics import run_target_diagnostics
from app.analysis_engine.model_simulation import run_model_simulation
from app.analysis_engine.structural_risk import run_structural_risk_analysis
from app.analysis_engine.recommendations import build_recommendations
from app.analysis_engine.scoring_v2 import compute_score_v2

logger = logging.getLogger(__name__)


def run_pipeline(

    file_path: str,
    target_column: str | None = None

):

    """
    Sentinel AI Analysis Pipeline.

    Responsible for:

    - loading dataframe
    - executing analyzers
    - aggregating report
    - graceful failure handling
    """

    report = {}

    failed_analyzers = []
   


    # Load Dataset

    try:

        df, ingestion_warnings = load_dataframe(file_path)
        profile = build_dataset_profile(df)

    except Exception as e:

        logger.exception(

            "Dataset loading failed"

        )

        raise RuntimeError(str(e))


    analyzers = [

        
        BasicStatsAnalyzer(),
        MissingAnalyzer(),
        ImbalanceAnalyzer(),    
        LeakageAnalyzer(),    
        OutlierAnalyzer(),
        CategoricalAnalyzer(),

    ]


    # Execute analyzers

    for analyzer in analyzers:

        try:

            result = analyzer.run(

                df,
                profile,
                target_column

            )

            report[analyzer.name] = result

        except Exception:

            logger.exception(

                f"{analyzer.name} failed"

            )

            failed_analyzers.append(

                analyzer.name

            )


    report["failed_analyzers"] = failed_analyzers
    report["ingestion"] = {
        "warnings": ingestion_warnings,
    }


    # V2 - target aware diagnostics
    target_diagnostics = run_target_diagnostics(df, target_column)
    report["target_diagnostics"] = target_diagnostics

    # V2 - modeling risk simulation
    task_type = target_diagnostics.get("task_type", "unknown")
    report["model_simulation"] = run_model_simulation(df, target_column, task_type)

    # V2 - structural risk
    report["structural_risk"] = run_structural_risk_analysis(df, target_column)

    # V2 - recommendations
    report["recommendations"] = build_recommendations(report)

    # V2-only scoring.
    score_v2, score_v2_meta = compute_score_v2(report)
    report["scores"] = {
        "v2": score_v2,
        "v2_meta": score_v2_meta,
    }

    report["summary"] = build_summary(report, score_v2, score_v2_meta)
    report["summary"]["dataset_difficulty"] = score_v2_meta.get("dataset_difficulty")
    report["summary"]["modeling_risk"] = score_v2_meta.get("modeling_risk")
    report["summary"]["recommended_actions"] = report.get("recommendations", {}).get(
        "top_actions", []
    )


  


    return report, score_v2
