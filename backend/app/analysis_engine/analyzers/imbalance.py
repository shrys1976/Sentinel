import pandas as pd
import logging

from pandas.io.pytables import dropna_doc
from app.analysis_engine.analyzers.base import BaseAnalyzer

logger = logging.getLogger(__name__)

class ImbalanceAnalyzer(BaseAnalyzer):
    name = "imbalance"

    def run(self,df: pd.DataFrame, target_column: str|None = None)-> dict :

        logger.info("Running imbalance analyzer")

        if not target_column:
            return{

                "skipped": True,
                "reason" :" no_target_column"
            }

        if target_column not in df.columns:
             raise ValueError(f"Target column {target_column} not found")

        target = df[target_column]

        value_counts = (

            target.value_counts(dropna =  False)
        .to_dict
        
        )       

        total = len(target)
        class_distribution = {
            str(k) : round(v/total, 4)
            for k, v in value_counts.items()
        }     
       


        minority_ratio = min(

            class_distribution.values()

        )


        imbalance_flag = minority_ratio < 0.1


        return {

            "target_column": target_column,

            "num_classes":

                len(class_distribution),

            "class_distribution":

                class_distribution,

            "minority_ratio":

                round(minority_ratio, 4),

            "imbalance_detected":

                imbalance_flag,

        }