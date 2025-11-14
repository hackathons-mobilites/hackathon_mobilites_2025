import logging
from datetime import datetime

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
) -> dict:
    departure_coordinates = source_handler.get_address_coordinates(address_name=departure_name)
    arrival_coordinates = source_handler.get_address_coordinates(address_name=arrival_name)
    logging.info(f"Departure coordinates: {departure_coordinates}, Arrival coordinates: {arrival_coordinates}")

    parking_coordinates = get_nearest_parking_velo(
        arrival_coordinates, filtre=parking_filter
    )["geometry"]
    logging.info(f"Parking coordinates: {parking_coordinates}")

    if to_parking:
        itinerary_velo = source_handler.get_itinerary_velo(departure_coordinates, parking_coordinates)
        itinerary_marche = source_handler.get_itinerary_marche(parking_coordinates, arrival_coordinates)
    else:
        itinerary_velo = source_handler.get_itinerary_velo(departure_coordinates, arrival_coordinates)
        itinerary_marche = None

    response: dict = {
        "itinerary_velo": itinerary_velo
    }

    if to_parking:
        response["itinerary_marche"] = itinerary_marche

    if get_forecast:
        response["meteo_forecast"] = get_meteo(travel_datetime)

    return response
