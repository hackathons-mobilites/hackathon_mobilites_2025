
from src.transports_possibles.domain.ports.file_system_handler import FileSystemHandler
from src.transports_possibles.domain.ports.source_handler import SourceHandler


def load_transports_possibles_data(source_handler: SourceHandler, file_system_handler: FileSystemHandler) -> None:
    df = source_handler.get_transports_possibles_data()
    file_system_handler.save_transports_possibles_data(df)
