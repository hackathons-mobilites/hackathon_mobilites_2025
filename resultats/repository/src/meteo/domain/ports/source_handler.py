from abc import ABC, abstractmethod
from datetime import datetime


class SourceHandler(ABC):
    @abstractmethod
    def fetch_meteo(self, datetime_depart: datetime) -> dict:
        pass
