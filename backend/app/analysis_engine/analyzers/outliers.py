import logging

import pandas as pd

from .base import BaseAnalyzer

logger = logging.getLogger(__name__)


class OutlierAnalyzer(BaseAnalyzer):
    name = "outliers"
    OUTLIER_RATIO_THRESHOLD = 0.05

    def run(self, df: pd.DataFrame, target_column: str | None = None) -> dict:
        logger.info("Running outlier analyzer")

        numeric_df = df.select_dtypes(include="number")
        if numeric_df.empty:
            return {"skipped": True, "reason": "no_numeric_columns"}

        q1 = numeric_df.quantile(0.25)
        q3 = numeric_df.quantile(0.75)
        iqr = q3 - q1

        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        outlier_ratios: dict[str, float] = {}
        for column in numeric_df.columns:
            col = numeric_df[column]

            if iqr[column] == 0 or pd.isna(iqr[column]):
                outlier_ratios[column] = 0.0
                continue

            mask = (col < lower_bound[column]) | (col > upper_bound[column])
            ratio = float(mask.mean()) if len(col) else 0.0
            outlier_ratios[column] = round(ratio, 4)

        high_outlier_columns = [
            col
            for col, ratio in outlier_ratios.items()
            if ratio >= self.OUTLIER_RATIO_THRESHOLD
        ]

        return {
            "threshold": self.OUTLIER_RATIO_THRESHOLD,
            "outlier_ratios": outlier_ratios,
            "high_outlier_columns": high_outlier_columns,
        }
