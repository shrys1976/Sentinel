import pandas as pd
from pandas.core.arrays import categorical
from app.analysis_engine.analyzers.base import BaseAnalyzer

class BasicStatsAnalyzer(BaseAnalyzer):
    name = "basic_stats"

    def run(

        self,
        df: pd.DataFrame,
        target_column : str | None = None
    ) -> dict:


        rows, columns = df.shape
        numeric_cols = df.select_dtypes(include="number").columns.to_list()
        categorical_cols = df.select_dtypes(exclude="number").columns.to_list()

        constant_columns = [

            col
            for col in df.columns
            if df[col].nunique(dropna=False) <=1
        ]

        duplicate_ratio = float(df.duplicate().mean())

        memory_mb  = float(df.memory_usage(deep=True).sum())/(1024*1024)

        dtype_counts = (

            df.dtypes.astype(str).value_counts().to_dict()
        )



        return {

            "rows": rows,
            "columns": columns,
            "numeric_columns":
                len(numeric_cols),
            "categorical_columns":
                len(categorical_cols),
            "constant_columns":
                constant_columns,
            "duplicate_ratio":
                duplicate_ratio,
            "dtype_distribution":
                dtype_counts,
            "estimated_memory_mb":

                round(memory_mb, 2),

        }

