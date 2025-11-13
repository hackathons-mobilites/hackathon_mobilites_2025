import geopandas as gpd
import os

from data import PATH_PARKING_VELO
from src.parking_velo.config.filters import ParkingVeloFilters
from src.parking_velo.domain.ports.file_system_handler import FileSystemHandler


class LocalFileSystemHandler(FileSystemHandler):

    def save_parking_velo_data(self, df: gpd.GeoDataFrame) -> None:
        df.to_parquet(PATH_PARKING_VELO, index=False)

    def get_parking_velo_data(self) -> gpd.GeoDataFrame:
        return gpd.read_parquet(PATH_PARKING_VELO)

    def save_filtered_parking_velo_data(self, df: gpd.GeoDataFrame, filter: ParkingVeloFilters) -> None:
        os.makedirs(os.path.dirname(filter.get_path()), exist_ok=True)
        df.to_parquet(filter.get_path(), index=False)

    def get_filtered_parking_velo_data(self, filter: ParkingVeloFilters) -> None:
        return gpd.read_parquet(filter.get_path())
