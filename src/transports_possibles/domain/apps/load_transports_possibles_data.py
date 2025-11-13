import logging
from src.transports_possibles.infrastructure.api_handler import ApiHandler
from src.transports_possibles.infrastructure.local_file_system_handler import LocalFileSystemHandler
from src.transports_possibles.domain.usecases.load_transports_possibles_data import load_transports_possibles_data


if __name__ == "__main__":
    logging.info("Loading transports possibles data...")

    api_handler = ApiHandler()
    local_fs_handler = LocalFileSystemHandler()

    load_transports_possibles_data(api_handler, local_fs_handler)
