from datetime import UTC, datetime
import logging

from src.meteo.domain.usecases.get_meteo_from_api import get_meteo_from_api
from src.meteo.infrastructure.api_handler import ApiHandler


def get_meteo(datetime_depart: datetime) -> dict:
    api_handler = ApiHandler()
    return get_meteo_from_api(api_handler, datetime_depart)


if __name__ == "__main__":
    current_datetime = datetime.now(UTC)
    current_meteo = get_meteo(datetime_depart=current_datetime)

    logging.info(current_meteo)


# Exemple retour :
# {'insee': '75056', 'cp': 75000, 'latitude': 48.8542, 'longitude': 2.3574, 'datetime': '2025-11-14T11:00:00+0100', 'temp2m': 17, 'rh2m': 50, 'wind10m': 8, 'gust10m': 30, 'dirwind10m': 166, 'rr10': 0.0, 'rr1': 0.0, 'probarain': 0, 'weather': 4, 'probafrost': 0, 'probafog': 0, 'probawind70': 0, 'probawind100': 0, 'tsoil1': 15, 'tsoil2': 14, 'gustx': 30, 'iso0': 2730}
