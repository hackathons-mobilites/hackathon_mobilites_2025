import geopandas as gpd

from src.parking_velo.config.filters import ParkingVeloFilters
from src.parking_velo.domain.ports.file_system_handler import FileSystemHandler


def get_parking_velo_data(file_system_handler: FileSystemHandler, filter: ParkingVeloFilters) -> gpd.GeoDataFrame:
    return file_system_handler.get_filtered_parking_velo_data(filter=filter)
