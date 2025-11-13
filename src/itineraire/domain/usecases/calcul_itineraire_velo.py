import logging

from src.parking_velo.config.filters import ParkingVeloFilters
from src.parking_velo.domain.apps.nearest_parking_velo import get_nearest_parking_velo
from src.itineraire.domain.ports.source_handler import SourceHandler


def calcul_itineraire_velo(source_handler: SourceHandler, departure_name: str, arrival_name: str) -> dict:
    departure_coordinates = source_handler.get_address_coordinates(address_name=departure_name)
    arrival_coordinates = source_handler.get_address_coordinates(address_name=arrival_name)
    logging.info(f"Departure coordinates: {departure_coordinates}, Arrival coordinates: {arrival_coordinates}")

    parking_coordinates = get_nearest_parking_velo(
        arrival_coordinates, filtre=ParkingVeloFilters.privee_abris
    )["geometry"]
    logging.info(f"Parking coordinates: {parking_coordinates}")

    itinerary_velo = source_handler.get_itinerary_velo(departure_coordinates, parking_coordinates)
    itinerary_marche = source_handler.get_itinerary_marche(parking_coordinates, arrival_coordinates)
    return {
        "itinerary_velo": itinerary_velo,
        "itinerary_marche": itinerary_marche
    }
