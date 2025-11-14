

from src.itineraire.domain.entities.velo_transportable import velo_transportable
from src.itineraire.domain.ports.source_handler import SourceHandler


def calcul_itineraire_transport(
        source_handler: SourceHandler, departure_name: str, arrival_name: str, travel_datetime: str | None, datetime_represents: str):
    
    if velo_transportable(travel_datetime):
        departure_coordinates = source_handler.get_address_coordinates(address_name=departure_name)
        arrival_coordinates = source_handler.get_address_coordinates(address_name=arrival_name)

        itinerary = source_handler.get_itinerary_transport(
            departure_coordinates, arrival_coordinates, travel_datetime, datetime_represents
        )
        return {
                "itinerary_transport": itinerary
        }

    return {
        "itinerary_transport": []
    }