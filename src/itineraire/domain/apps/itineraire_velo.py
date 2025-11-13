import logging

from src.itineraire.domain.usecases.calcul_itineraire_velo import calcul_itineraire_velo
from src.itineraire.infrastructure.api_handler import ApiHandler


def itineraire_parking_velo(departure_address: str, arrival_address: str) -> dict:
    api_handler = ApiHandler()
    itinerary = calcul_itineraire_velo(api_handler, departure_address, arrival_address)
    return itinerary


if __name__ == "__main__":
    itinerary = itineraire_parking_velo("34 avenue de l'opera", "62 Rue Jean-Jacques Rousseau")
    logging.info(itinerary.get("itinerary_marche"))
