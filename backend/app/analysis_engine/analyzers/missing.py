import pandas as pd
import logging

from pandas.io.pytables import Col
from app.analysis_engine.analyzers.base import BaseAnalyzer
logger = logging.getLogger(__name__)

class MissingAnalyzer(BaseAnalyzer):
    name = "missing"

    def run(self,df:pd.DataFrame,target_column: str | None = None)-> dict:

        logger.info("Running missing analyzer")
        total_rows = len(df)

        missing_ratio = (df.isnull().mean().round(4).to_dict())

        fully_null_columns = [col for col,ratio in missing_ratio.item() if ratio == 1.0]

        high_missing_columns = [col for col, ratio  in missing_ratio.item() if ratio>=0.5]

        overall_missing_ratio = float(df.isnull().sum().sum())/(df.shape[0]*df.shape[1])

        return {

            "overall_missing_ratio":

                round(overall_missing_ratio, 4),

            "missing_ratio":

                missing_ratio,

            "fully_null_columns":

                fully_null_columns,

            "high_missing_columns":

                high_missing_columns,

        }
