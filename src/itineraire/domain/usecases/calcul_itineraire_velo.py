import logging
from datetime import datetime

from shapely import Point

from src.itineraire.domain.apps.itineraire_transport_velo_autorise import itineraire_transport_velo_autorise
from src.itineraire.domain.entities.velo_transportable import velo_transportable
from src.parking_velo.config.filters import ParkingVeloFilters
from src.parking_velo.domain.apps.nearest_parking_velo import get_nearest_parking_velo
from src.itineraire.domain.ports.source_handler import SourceHandler
from src.meteo.domain.apps.get_meteo import get_meteo


def calcul_itineraire_velo(
    source_handler: SourceHandler,
    departure_name: str,
    arrival_name: str,
    to_parking: bool,
    parking_filter: ParkingVeloFilters,
    travel_datetime: datetime,
    get_forecast: bool = False,
    use_train: bool = True,
) -> dict:
    departure_coordinates = source_handler.get_address_coordinates(address_name=departure_name)
    arrival_coordinates = source_handler.get_address_coordinates(address_name=arrival_name)
    logging.info(f"Departure coordinates: {departure_coordinates}, Arrival coordinates: {arrival_coordinates}")

    itinerary_velo = []
    itineraire_transport = []
    itinerary_marche = []
    sections_public_transport = []

    parking_coordinates = get_nearest_parking_velo(
        arrival_coordinates, filtre=parking_filter
    )["geometry"]
    logging.info(f"Parking coordinates: {parking_coordinates}")

    if use_train:
        journeys = source_handler.get_itinerary_transport(
            departure_coordinates, arrival_coordinates, travel_datetime, travel_datetime.strftime("%Y%m%dT%H%M%S")
        )
        authorized_journeys = []

        for journey in journeys:
            transportable = True
            sections_public_transport = journey.get("sections")
            for section in sections_public_transport:
                mode = section.get('type')
                if mode == "public_transport":
                    time = section.get('departure_date_time')
                    if not velo_transportable(time):
                        transportable = False
            if transportable:
                authorized_journeys.append(journey)

        itineraire_transport = authorized_journeys[0] if authorized_journeys else []
    else:
        itineraire_transport = []

    if itineraire_transport:
        sections_public_transport = []
        for section in itineraire_transport.get("sections", []):
            if section.get("type") == "public_transport":
                sections_public_transport.append(section)
        logging.info("Authorized transport itinerary found.")

    if sections_public_transport:

        logging.info("The itinerary includes public transport sections where bikes are allowed.")
        transportation_departure_coordinates = Point(
            float(sections_public_transport[0]["from"]["stop_point"]["coord"]["lon"]),
            float(sections_public_transport[0]["from"]["stop_point"]["coord"]["lat"]),
        )
        transportation_arrival_coordinates = Point(
            float(sections_public_transport[-1]["to"]["stop_point"]["coord"]["lon"]),
            float(sections_public_transport[-1]["to"]["stop_point"]["coord"]["lat"]),
        )

        itinerary_velo.append(
            source_handler.get_itinerary_velo(departure_coordinates, transportation_departure_coordinates)
        )

        departure_coordinates = transportation_arrival_coordinates

    if to_parking:
        itinerary_velo.append(source_handler.get_itinerary_velo(departure_coordinates, parking_coordinates))
        itinerary_marche.append(source_handler.get_itinerary_marche(parking_coordinates, arrival_coordinates))
    else:
        itinerary_velo.append(source_handler.get_itinerary_velo(departure_coordinates, arrival_coordinates))
        itinerary_marche = None

    response: dict = {
        "itinerary_velo": itinerary_velo,
        "itinerary_transport": sections_public_transport,
    }

    if to_parking:
        response["itinerary_marche"] = itinerary_marche

    if get_forecast:
        response["meteo_forecast"] = get_meteo(travel_datetime)

    return response
