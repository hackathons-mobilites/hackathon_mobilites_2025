import datetime
import logging

from src.itineraire.domain.usecases.calcul_itineraire_transport import \
    calcul_itineraire_transport
from src.itineraire.infrastructure.api_handler import ApiHandler
from src.parking_velo.config.filters import ParkingVeloFilters


def itineraire_transport_velo_autorise(
        departure_address: str, 
        arrival_address: str, 
        travel_datetime: datetime = None, 
        datetime_representss: str = "departure"
    ) -> dict:
    api_handler = ApiHandler()
    itinerary = calcul_itineraire_transport(
        api_handler, departure_address, arrival_address, travel_datetime, datetime_representss)
    return itinerary


if __name__ == "__main__":
    itinerary = itineraire_transport_velo_autorise(
        "34 avenue de l'opera", "Cergy"
    )
    print(itinerary)
    logging.info(itinerary.get("itinerary_transport"))
