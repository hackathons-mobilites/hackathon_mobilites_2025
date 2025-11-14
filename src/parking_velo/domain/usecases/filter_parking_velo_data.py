from src.parking_velo.config.filters import ParkingVeloFilters
from src.parking_velo.config.columns import ParkingVeloColumns
from src.parking_velo.domain.ports.file_system_handler import FileSystemHandler
import geopandas as gpd
from typing import Callable

FILTER_LIST: list[tuple[str, Callable[[gpd.GeoDataFrame], gpd.GeoDataFrame]]] = [
    (
        ParkingVeloFilters.privee_abris,
        lambda df: df[
            (df[ParkingVeloColumns.acces] == "privee")
            & (df[ParkingVeloColumns.type] == "abri")
        ]
    ),
    (
        ParkingVeloFilters.clientele_abris,
        lambda df: df[
            (df[ParkingVeloColumns.acces] == "clientele")
            & (df[ParkingVeloColumns.type] == "abri")
        ]
    ),
    (
        ParkingVeloFilters.casier,
        lambda df: df[
            (df[ParkingVeloColumns.type] == "casier")
        ]
    ),
    (
        ParkingVeloFilters.surveille,
        lambda df: df[
            (df[ParkingVeloColumns.surveille] == "OUI")
        ]
    ),
    (
        ParkingVeloFilters.default,
        lambda df: df[
            ((df[ParkingVeloColumns.acces] == "privee") & (df[ParkingVeloColumns.type] == "abri")) |
            ((df[ParkingVeloColumns.acces] == "clientele") & (df[ParkingVeloColumns.type] == "abri")) |
            (df[ParkingVeloColumns.type] == "casier") |
            (df[ParkingVeloColumns.surveille] == "OUI")
        ]
    ),
]


def filter_parking_velo_data(
    file_system_handler: FileSystemHandler,
) -> gpd.GeoDataFrame:

    df_gpd_parking_velo = file_system_handler.get_parking_velo_data()
    print(df_gpd_parking_velo)
    for filter, filter_function in FILTER_LIST:
        filtered_df_gpd = df_gpd_parking_velo.copy()
        filtered_df_gpd = filter_function(filtered_df_gpd)

        file_system_handler.save_filtered_parking_velo_data(filtered_df_gpd, filter)
