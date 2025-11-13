import geopandas as gpd

from abc import ABC, abstractmethod


class FileSystemHandler(ABC):
    @abstractmethod
    def save_parking_velo_data(self, df: gpd.GeoDataFrame) -> None:
        pass

    @abstractmethod
    def get_parking_velo_data(self) -> gpd.GeoDataFrame:
        pass
