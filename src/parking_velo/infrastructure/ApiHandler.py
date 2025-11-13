from urllib.parse import urljoin

import pandas as pd

from src.parking_velo.domain.ports.SourceHandler import SourceHandler

OPEN_DATA_BASE_URL = "https://data.iledefrance-mobilites.fr/api/explore/v2.1/catalog/datasets/"

URL_PARKING_VELO = urljoin(
    OPEN_DATA_BASE_URL,
    "stationnement-velo-en-ile-de-france/exports/parquet?lang=fr&timezone=Europe%2FBerlin"
)


class ApiHandler(SourceHandler):
    def get_parking_velo_data(self) -> pd.DataFrame:
        return pd.read_parquet(URL_PARKING_VELO)
