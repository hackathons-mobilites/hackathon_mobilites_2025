import logging
from parking_velo.infrastructure.api_handler import ApiHandler
from parking_velo.infrastructure.local_file_system_handler import LocalFileSystemHandler
from src.parking_velo.domain.usecases.load_parking_velo_data import load_parking_velo_data


if __name__ == "__main__":
    logging.info("Loading parking vélo data...")

    api_handler = ApiHandler()
    local_fs_handler = LocalFileSystemHandler()

    load_parking_velo_data(api_handler, local_fs_handler)
