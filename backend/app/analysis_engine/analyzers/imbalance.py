import logging

import pandas as pd

from .base import BaseAnalyzer

logger = logging.getLogger(__name__)


class ImbalanceAnalyzer(BaseAnalyzer):
    name = "imbalance"

    def run(
        self,
        df: pd.DataFrame,
        profile: dict,
        target_column: str | None = None,
    ) -> dict:
        logger.info("Running imbalance analyzer")

        if df.empty:
            return {"skipped": True, "reason": "empty_dataframe"}

        if not target_column:
            return {"skipped": True, "reason": "no_target_column"}

        if target_column not in df.columns:
            raise ValueError(f"Target column {target_column} not found")

        target = df[target_column]
        total = len(target)
        if total == 0:
            return {
                "target_column": target_column,
                "num_classes": 0,
                "class_distribution": {},
                "minority_ratio": 0.0,
                "imbalance_detected": False,
            }

        value_counts = target.value_counts(dropna=False).to_dict()
        class_distribution = {
            str(k): round(float(v / total), 4) for k, v in value_counts.items()
        }

        minority_ratio = min(class_distribution.values()) if class_distribution else 0.0
        imbalance_flag = minority_ratio < 0.1 if class_distribution else False

        return {
            "target_column": target_column,
            "num_classes": len(class_distribution),
            "class_distribution": class_distribution,
            "minority_ratio": round(float(minority_ratio), 4),
            "imbalance_detected": imbalance_flag,
        }
