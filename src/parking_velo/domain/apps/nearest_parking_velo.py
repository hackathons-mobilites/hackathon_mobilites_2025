import geopandas as gpd
from shapely.geometry import Point

from parking_velo.domain.usecases.find_nearest_parking_velo import find_nearest_parking_velo
from src.parking_velo.infrastructure.LocalFileSystemHandler import LocalFileSystemHandler


def get_nearest_parking_velo(point: Point) -> gpd.GeoSeries:
    local_file_system_handler = LocalFileSystemHandler()
    return find_nearest_parking_velo(local_file_system_handler, point)


if __name__ == "__main__":
    point = Point(2.3522, 48.8566)

    get_nearest_parking_velo(point)
