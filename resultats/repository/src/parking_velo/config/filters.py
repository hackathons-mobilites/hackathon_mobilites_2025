from enum import Enum
from posixpath import join

from data import FILTERED_DATA_PATH


class ParkingVeloFilters(str, Enum):
    privee_abris = 'privee_abris'
    clientele_abris = 'clientele_abris'
    casier = 'casier'
    surveille = 'surveille'
    default = 'default'

    def get_path(self) -> str:
        return join(FILTERED_DATA_PATH, f"parking_velo_filter_{self.value}.parquet")

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return self.value
