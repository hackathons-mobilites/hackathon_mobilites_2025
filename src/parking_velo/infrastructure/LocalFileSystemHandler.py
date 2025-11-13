from posixpath import join

import pandas as pd

from data import DATA_PATH
from src.parking_velo.domain.ports.FileSystemHandler import FileSystemHandler


PATH_PARKING_VELO = join(DATA_PATH, "parking_velo.parquet")


class LocalFileSystemHandler(FileSystemHandler):

    def save_parking_velo_data(self, df: pd.DataFrame) -> None:
        df.to_parquet(PATH_PARKING_VELO, index=False)

    def get_parking_velo_data(self) -> pd.DataFrame:
        return pd.read_parquet(PATH_PARKING_VELO)
