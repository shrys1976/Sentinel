import pandas as pd
import logging

from app.analysis_engine.analyzers.base import BaseAnalyzer


logger = logging.getLogger(__name__)


class CategoricalAnalyzer(BaseAnalyzer):

    name = "categorical"

    HIGH_CARDINALITY_THRESHOLD = 0.5


    def run(

        self,

        df: pd.DataFrame,

        target_column: str | None = None

    ) -> dict:

        logger.info("Running categorical analyzer")


        categorical_df = df.select_dtypes(

            exclude="number"

        )


        if categorical_df.empty:

            return {

                "skipped": True,

                "reason":

                "no_categorical_columns"

            }


        rows = len(df)

        unique_ratio = {}
        high_cardinality_columns = []
        constant_columns = []

        for column in categorical_df.columns:

            unique_count = df[column].nunique(
                dropna=False

            )

            ratio = unique_count / rows
            unique_ratio[column] = round(

                float(ratio),

                4

            )


            if ratio >= self.HIGH_CARDINALITY_THRESHOLD:
                high_cardinality_columns.append(
                    column

                )


            if unique_count <= 1:
                constant_columns.append(
                    column

                )


        return {

            "threshold":

                self.HIGH_CARDINALITY_THRESHOLD,

            "unique_ratio":

                unique_ratio,

            "high_cardinality_columns":

                high_cardinality_columns,

            "constant_columns":

                constant_columns,

        }