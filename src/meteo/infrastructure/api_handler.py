from datetime import datetime

import requests

from config.var_env import METEO_API_KEY
from src.meteo.domain.ports.source_handler import SourceHandler


class ApiHandler(SourceHandler):
    def fetch_meteo(self, datetime_depart: datetime) -> dict:
        url = "https://api.meteo-concept.com/api/forecast/nextHours"
        params = {
            "token": METEO_API_KEY,
            "insee": 75056
        }
        response = requests.get(url, params=params)

        forecast_data = response.json()

        datetime_list = [
            abs(
                (datetime.fromisoformat(forecast["datetime"]) - datetime_depart).total_seconds()
            ) for forecast in forecast_data.get("forecast", [])
        ]
        min_index = datetime_list.index(min(datetime_list))

        return forecast_data["forecast"][min_index]
