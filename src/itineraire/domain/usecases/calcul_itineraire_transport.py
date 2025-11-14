

from src.itineraire.domain.entities.velo_transportable import velo_transportable
from src.itineraire.domain.ports.source_handler import SourceHandler


def calcul_itineraire_transport(
        source_handler: SourceHandler, departure_name: str, arrival_name: str, travel_datetime: str | None, datetime_represents: str):

    departure_coordinates = source_handler.get_address_coordinates(address_name=departure_name)
    arrival_coordinates = source_handler.get_address_coordinates(address_name=arrival_name)

    journeys = source_handler.get_itinerary_transport(
        departure_coordinates, arrival_coordinates, travel_datetime, datetime_represents
    )
    authorized_journeys = []

    for journey in journeys:
        transportable = True
        sections = journey.get("sections")
        for section in sections:
            mode = section.get('type')
            if mode=="public_transport":
                time = section.get('departure_date_time')
                if not velo_transportable(time):
                    transportable = False
        if transportable:
            authorized_journeys.append(journey)

    return {
        "itinerary_transport": authorized_journeys
    }
