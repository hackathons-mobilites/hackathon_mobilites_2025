import geopandas as gpd

from data import PATH_PARKING_VELO
from src.parking_velo.domain.ports.FileSystemHandler import FileSystemHandler


class LocalFileSystemHandler(FileSystemHandler):

    def save_parking_velo_data(self, df: gpd.GeoDataFrame) -> None:
        df.to_parquet(PATH_PARKING_VELO, index=False)

    def get_parking_velo_data(self) -> gpd.GeoDataFrame:
        return gpd.read_parquet(PATH_PARKING_VELO)
