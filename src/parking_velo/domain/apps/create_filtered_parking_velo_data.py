import logging
from src.parking_velo.infrastructure.local_file_system_handler import LocalFileSystemHandler
from src.parking_velo.domain.usecases.filter_parking_velo_data import filter_parking_velo_data


if __name__ == "__main__":
    logging.info("Filtering parking vélo data...")

    local_fs_handler = LocalFileSystemHandler()

    filtered_data = filter_parking_velo_data(local_fs_handler)

    logging.info("Filtered data saved successfully.")
