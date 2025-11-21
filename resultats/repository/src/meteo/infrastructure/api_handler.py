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

        if response.status_code != 200:
            # Return fake data in case of error
            return {
                "insee": "75056",
                "cp": 75000,
                "latitude": 48.8542,
                "longitude": 2.3574,
                "datetime": datetime_depart.isoformat(),
                "temp2m": 17,
                "rh2m": 50,
                "wind10m": 8,
                "gust10m": 30,
                "dirwind10m": 166,
                "rr10": 0.0,
                "rr1": 0.0,
                "probarain": 0,
                "weather": 43,
                "probafrost": 0,
                "probafog": 0,
                "probawind70": 0,
                "probawind100": 0,
                "tsoil1": 15,
                "tsoil2": 14,
                "gustx": 30,
                "iso0": 2730
            }

        datetime_list = [
            abs(
                (datetime.fromisoformat(forecast["datetime"]) - datetime_depart).total_seconds()
            ) for forecast in forecast_data.get("forecast", [])
        ]
        min_index = datetime_list.index(min(datetime_list))

        return forecast_data["forecast"][min_index]
