

from src.itineraire.domain.usecases.calcul_itineraire_velo import calcul_itineraire_velo
from src.itineraire.infrastructure.api_handler import ApiHandler


def itineraire_parking_velo(departure_address: str, arrival_address: str) -> dict:


    source_handler = ApiHandler()
    itinerary = calcul_itineraire_velo(source_handler, departure_address, arrival_address)
    return itinerary


if __name__=="__main__":
    i = itineraire_parking_velo("34 avenue de l'opera", "62 Rue Jean-Jacques Rousseau")