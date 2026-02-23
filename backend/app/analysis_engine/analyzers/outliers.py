import pandas as pd
import logging

from app.analysis_engine.analyzers.base import BaseAnalyzer


logger = logging.getLogger(__name__)


class OutlierAnalyzer(BaseAnalyzer):

    name = "outliers"
    OUTLIER_RATIO_THRESHOLD = 0.05
    def run(

        self,
        df: pd.DataFrame,
        target_column: str | None = None

    ) -> dict:

        logger.info("Running outlier analyzer")
        numeric_df = df.select_dtypes(

            include="number"
        )

        if numeric_df.empty:
            return {

                "skipped": True,
                "reason":
                "no_numeric_columns"
            }


        Q1 = numeric_df.quantile(0.25)
        Q3 = numeric_df.quantile(0.75)

        IQR = Q3 - Q1

        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        outlier_ratios = {}


        for column in numeric_df.columns:

            col = numeric_df[column]
            mask = (

                (col < lower_bound[column])

                |

                (col > upper_bound[column])

            )


            ratio = float(mask.mean())
            outlier_ratios[column] = round(
                ratio,
                4

            )


        high_outlier_columns = [
            col
            for col, ratio in outlier_ratios.items()
            if ratio >= self.OUTLIER_RATIO_THRESHOLD

        ]
        return {

            "threshold":

                self.OUTLIER_RATIO_THRESHOLD,

            "outlier_ratios":

                outlier_ratios,

            "high_outlier_columns":

                high_outlier_columns,

        }