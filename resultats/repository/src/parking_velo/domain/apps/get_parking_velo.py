import logging

import geopandas as gpd

from src.parking_velo.domain.usecases.get_parking_velo_data import get_parking_velo_data
from src.parking_velo.config.filters import ParkingVeloFilters
from src.parking_velo.infrastructure.local_file_system_handler import LocalFileSystemHandler


def get_parking_velo(filter: ParkingVeloFilters) -> gpd.GeoDataFrame:
    local_fs_handler = LocalFileSystemHandler()
    return get_parking_velo_data(file_system_handler=local_fs_handler, filter=filter)


if __name__ == "__main__":
    logging.info("Get parking velo data filtered...")
    get_parking_velo(filter=ParkingVeloFilters.privee_abris)
