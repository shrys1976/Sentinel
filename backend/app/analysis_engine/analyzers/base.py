from abc import ABC, abstractmethod
import pandas as pd

class BaseAnalyzer(ABC):

    name = "base"

    @abstractmethod
    def run(

        self,
        df: pd.DataFrame,
        profile: dict,
        target_column: str | None = None
    ) -> dict:

        pass
