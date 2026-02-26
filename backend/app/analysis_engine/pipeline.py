import logging

from app.analysis_engine.scoring import compute_score
from app.analysis_engine.data_loader import load_dataframe
from app.analysis_engine.analyzers.basic_stats import BasicStatsAnalyzer
from app.analysis_engine.analyzers.missing import MissingAnalyzer
from app.analysis_engine.analyzers.imbalance import ImbalanceAnalyzer
from app.analysis_engine.analyzers.leakage import LeakageAnalyzer
from app.analysis_engine.analyzers.outliers import OutlierAnalyzer
from app.analysis_engine.analyzers.categorical import CategoricalAnalyzer
from app.analysis_engine.scoring import compute_score
from app.analysis_engine.summary import build_summary
from app.analysis_engine.profile import build_dataset_profile

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


    # Temporary score
    score, summary = compute_score(report)

    report["summary"] = build_summary(report,score,summary)


  


    return report, score
