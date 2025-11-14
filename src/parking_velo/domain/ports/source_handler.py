from abc import ABC, abstractmethod

import pandas as pd


class SourceHandler(ABC):
    @abstractmethod
    def get_parking_velo_data(self) -> pd.DataFrame:
        pass
