import logging
from datetime import UTC, datetime
from typing import Optional

from src.parking_velo.config.filters import ParkingVeloFilters
from src.itineraire.domain.usecases.calcul_itineraire_velo import calcul_itineraire_velo
from src.itineraire.infrastructure.api_handler import ApiHandler


def itineraire_parking_velo(
    departure_address: str,
    arrival_address: str,
    to_parking: bool,
    travel_datetime: Optional[datetime] = None,
    get_forecast: bool = True,
    parking_filter: ParkingVeloFilters = ParkingVeloFilters.default,
    use_train: bool = True,
) -> dict:
    api_handler = ApiHandler()

    if travel_datetime:
        if travel_datetime.tzinfo is None:
            raise ValueError("travel_datetime doit être en timezone UTC")
    else:
        travel_datetime = datetime.now(UTC)

    itinerary = calcul_itineraire_velo(
        source_handler=api_handler,
        departure_name=departure_address,
        arrival_name=arrival_address,
        to_parking=to_parking,
        parking_filter=parking_filter,
        travel_datetime=travel_datetime,
        get_forecast=get_forecast,
        use_train=use_train,
    )
    return itinerary


if __name__ == "__main__":
    itinerary = itineraire_parking_velo(
        departure_address="34 avenue de l'opera",
        arrival_address="Cergy",
        to_parking=True,
        travel_datetime=None,
        get_forecast=True,
        parking_filter=ParkingVeloFilters.casier,
        use_train=True,
    )
    print(itinerary)
    logging.info(itinerary)
