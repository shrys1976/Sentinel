import logging

import pandas as pd

from .base import BaseAnalyzer

logger = logging.getLogger(__name__)


class MissingAnalyzer(BaseAnalyzer):
    name = "missing"

    def run(self, df: pd.DataFrame, target_column: str | None = None) -> dict:
        logger.info("Running missing analyzer")

        rows, cols = df.shape
        if rows == 0 or cols == 0:
            return {
                "overall_missing_ratio": 0.0,
                "missing_ratio": {},
                "fully_null_columns": [],
                "high_missing_columns": [],
            }

        missing_ratio = df.isnull().mean().round(4).to_dict()

        fully_null_columns = [
            col for col, ratio in missing_ratio.items() if float(ratio) == 1.0
        ]
        high_missing_columns = [
            col for col, ratio in missing_ratio.items() if float(ratio) >= 0.5
        ]

        overall_missing_ratio = float(df.isnull().sum().sum()) / float(rows * cols)

        return {
            "overall_missing_ratio": round(overall_missing_ratio, 4),
            "missing_ratio": missing_ratio,
            "fully_null_columns": fully_null_columns,
            "high_missing_columns": high_missing_columns,
        }
