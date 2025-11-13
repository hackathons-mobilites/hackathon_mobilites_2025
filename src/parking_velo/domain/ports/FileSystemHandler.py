import pandas as pd


from abc import ABC, abstractmethod


class FileSystemHandler(ABC):
    @abstractmethod
    def save_parking_velo_data(self, df: pd.DataFrame) -> None:
        pass

    @abstractmethod
    def get_parking_velo_data(self) -> pd.DataFrame:
        pass
