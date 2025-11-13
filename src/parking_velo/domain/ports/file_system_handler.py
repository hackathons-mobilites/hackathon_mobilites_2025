import geopandas as gpd

from abc import ABC, abstractmethod

from src.parking_velo.config.filters import ParkingVeloFilters


class FileSystemHandler(ABC):
    @abstractmethod
    def save_parking_velo_data(self, df: gpd.GeoDataFrame) -> None:
        pass

    @abstractmethod
    def get_parking_velo_data(self) -> gpd.GeoDataFrame:
        pass

    @abstractmethod
    def save_filtered_parking_velo_data(self, df: gpd.GeoDataFrame, filter: ParkingVeloFilters) -> None:
        pass

    @abstractmethod
    def get_filtered_parking_velo_data(self, filter: ParkingVeloFilters) -> None:
        pass
