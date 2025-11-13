import pandas as pd

from data import PATH_TRANSPORTS_POSSIBLES
from src.transports_possibles.domain.ports.file_system_handler import FileSystemHandler


class LocalFileSystemHandler(FileSystemHandler):

    def save_transports_possibles_data(self, df: pd.DataFrame) -> None:
        df.to_parquet(PATH_TRANSPORTS_POSSIBLES, index=False)

    def get_transports_possibles_data(self) -> pd.DataFrame:
        return pd.read_parquet(PATH_TRANSPORTS_POSSIBLES)
