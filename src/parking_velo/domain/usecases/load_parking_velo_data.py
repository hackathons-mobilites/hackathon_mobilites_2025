from src.parking_velo.domain.entities.parking_velo_to_gpd import parking_velo_to_gpd
from src.parking_velo.domain.ports.file_system_handler import FileSystemHandler
from src.parking_velo.domain.ports.source_handler import SourceHandler


def load_parking_velo_data(source_handler: SourceHandler, file_system_handler: FileSystemHandler) -> None:
    df = source_handler.get_parking_velo_data()
    df_gpd = parking_velo_to_gpd(df)
    file_system_handler.save_parking_velo_data(df_gpd)
