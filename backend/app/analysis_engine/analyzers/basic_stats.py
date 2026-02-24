import pandas as pd

from .base import BaseAnalyzer


class BasicStatsAnalyzer(BaseAnalyzer):
    name = "basic_stats"

    def run(
        self,
        df: pd.DataFrame,
        profile: dict,
        target_column: str | None = None,
    ) -> dict:
        rows = profile["rows"]
        columns = profile["columns"]
        numeric_cols = df.select_dtypes(include="number").columns.to_list()
        categorical_cols = df.select_dtypes(exclude="number").columns.to_list()

        constant_columns = [
            col for col in df.columns if df[col].nunique(dropna=False) <= 1
        ]

        duplicate_ratio = float(df.duplicated().mean()) if rows else 0.0
        memory_mb = float(df.memory_usage(deep=True).sum()) / (1024 * 1024)

        dtype_counts = df.dtypes.astype(str).value_counts().to_dict()

        return {
            "rows": int(rows),
            "columns": int(columns),
            "numeric_columns": int(len(numeric_cols)),
            "categorical_columns": int(len(categorical_cols)),
            "constant_columns": constant_columns,
            "duplicate_ratio": round(duplicate_ratio, 4),
            "dtype_distribution": dtype_counts,
            "estimated_memory_mb": round(memory_mb, 2),
        }
