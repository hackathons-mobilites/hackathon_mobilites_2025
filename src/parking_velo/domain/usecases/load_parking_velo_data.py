from src.parking_velo.domain.ports.FileSystemHandler import FileSystemHandler
from src.parking_velo.domain.ports.SourceHandler import SourceHandler


def load_parking_velo_data(source_handler: SourceHandler, file_system_handler: FileSystemHandler) -> None:
    df = source_handler.get_parking_velo_data()
    file_system_handler.save_parking_velo_data(df)
