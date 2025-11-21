from abc import ABC, abstractmethod

import pandas as pd


class SourceHandler(ABC):
    @abstractmethod
    def get_transports_possibles_data(self) -> pd.DataFrame:
        pass
