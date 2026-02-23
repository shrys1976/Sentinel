import logging

from app.analysis_engine.data_loader import load_dataframe
from app.analysis_engine.analyzers.basic_stats import BasicStatsAnalyzer
from app.analysis_engine.analyzers.missing import MissingAnalyzer

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

        df = load_dataframe(file_path)

    except Exception as e:

        logger.exception(

            "Dataset loading failed"

        )

        raise RuntimeError(str(e))


    analyzers = [

        
        BasicStatsAnalyzer(),
        MissingAnalyzer()
        

    ]


    # Execute analyzers

    for analyzer in analyzers:

        try:

            result = analyzer.run(

                df,

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


    # Temporary score

    score = 100


    return report, score