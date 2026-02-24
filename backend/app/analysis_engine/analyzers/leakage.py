import logging

import pandas as pd

from .base import BaseAnalyzer

logger = logging.getLogger(__name__)


class LeakageAnalyzer(BaseAnalyzer):
    name = "leakage"
    CORRELATION_THRESHOLD = 0.9

    def run(self, df: pd.DataFrame, target_column: str | None = None) -> dict:
        logger.info("Running leakage analyzer")

        if df.empty:
            return {"skipped": True, "reason": "empty_dataframe"}

        if not target_column:
            return {"skipped": True, "reason": "no_target_column"}

        if target_column not in df.columns:
            raise ValueError(f"Target column '{target_column}' not found")

        numeric_df = df.select_dtypes(include="number")
        if target_column not in numeric_df.columns:
            return {"skipped": True, "reason": "target_not_numeric"}

        correlations = (
            numeric_df.corr(numeric_only=True)[target_column].drop(labels=[target_column])
        )

        suspicious_features: dict[str, float] = {}
        for feature, corr in correlations.items():
            if pd.isna(corr):
                continue
            if abs(corr) >= self.CORRELATION_THRESHOLD:
                suspicious_features[feature] = round(float(corr), 4)

        leakage_detected = len(suspicious_features) > 0

        return {
            "target_column": target_column,
            "threshold": self.CORRELATION_THRESHOLD,
            "suspicious_features": suspicious_features,
            "leakage_detected": leakage_detected,
        }
