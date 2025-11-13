import geopandas as gpd
from shapely.geometry import Point

from src.parking_velo.domain.entities.nearest_parking_velo import nearest_parking_velo
from src.parking_velo.domain.ports.FileSystemHandler import FileSystemHandler


def find_nearest_parking_velo(file_system_handler: FileSystemHandler, point: Point) -> gpd.GeoSeries:
    df_gpd_parking_velo = file_system_handler.get_parking_velo_data()

    return nearest_parking_velo(df_gpd_parking_velo, point)
