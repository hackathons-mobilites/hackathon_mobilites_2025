from datetime import datetime

from src.meteo.domain.ports.source_handler import SourceHandler


def get_meteo_from_api(api_handler: SourceHandler, datetime_depart: datetime) -> dict:
    return api_handler.fetch_meteo(datetime_depart)
