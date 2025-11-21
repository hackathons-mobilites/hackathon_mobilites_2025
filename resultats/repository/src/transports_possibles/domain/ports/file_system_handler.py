import pandas as pd

from abc import ABC, abstractmethod


class FileSystemHandler(ABC):
    @abstractmethod
    def save_transports_possibles_data(self, df: pd.DataFrame) -> None:
        pass

    @abstractmethod
    def get_transports_possibles_data(self) -> pd.DataFrame:
        pass
