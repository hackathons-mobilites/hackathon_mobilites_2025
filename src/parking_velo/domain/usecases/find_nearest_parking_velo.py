import geopandas as gpd
from shapely.geometry import Point

from src.parking_velo.config.filters import ParkingVeloFilters
from src.parking_velo.domain.entities.nearest_parking_velo import nearest_parking_velo
from src.parking_velo.domain.ports.file_system_handler import FileSystemHandler


def find_nearest_parking_velo(file_system_handler: FileSystemHandler, point: Point, filtre: ParkingVeloFilters) -> gpd.GeoSeries:
    df_gpd_parking_velo = file_system_handler.get_filtered_parking_velo_data(filtre)

    return nearest_parking_velo(df_gpd_parking_velo, point)
