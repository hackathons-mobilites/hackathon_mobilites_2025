import datetime
import json
from urllib.parse import urljoin

import pyproj
import requests
from shapely.geometry import Point

from config.var_env import (API_KEY_PRIM, BASE_URL_PRIM, PATH_CALCULATEUR_IDFM,
                            PATH_GEOVELO)
from src.itineraire.domain.ports.source_handler import SourceHandler


class ApiHandler(SourceHandler):
    def __init__(self):
        self.url_prim = urljoin(BASE_URL_PRIM, PATH_CALCULATEUR_IDFM)

        self.url_geovelo = urljoin(BASE_URL_PRIM, PATH_GEOVELO)

        self.headers = {'apiKey': API_KEY_PRIM}
        self.session = requests.Session()

        self.session.headers.update(self.headers)

        # Configuration de la transformation Lambert II étendu -> WGS84
        self.lambert_to_wgs84 = pyproj.Transformer.from_crs(
            "EPSG:27572",  # Lambert II étendu
            "EPSG:4326",   # WGS84 (latitude/longitude)
            always_xy=True
        )

    def get_address_coordinates(self, address_name: str) -> Point:
        params = {'q': address_name}
        r = self.session.get(f"{self.url_geovelo}/places", params=params)

        # Vérifications de sécurité
        response_data = r.json()
        if not response_data:
            raise ValueError(f"Aucune réponse de l'API pour l'adresse: {address_name}")

        places = response_data.get('places')
        if not places or len(places) == 0:
            raise ValueError(f"Aucun lieu trouvé pour l'adresse: {address_name}")

        place = places[0]

        # Utiliser les coordonnées x, y en Lambert II étendu
        lambert_x = place.get('x')
        lambert_y = place.get('y')

        if lambert_x is None or lambert_y is None:
            raise ValueError(f"Coordonnées Lambert manquantes pour l'adresse: {address_name}")

        # Conversion Lambert II étendu -> WGS84
        try:
            wgs84_lon, wgs84_lat = self.lambert_to_wgs84.transform(lambert_x, lambert_y)
            return Point(wgs84_lon, wgs84_lat)
        except Exception as e:
            raise ValueError(f"Erreur conversion coordonnées pour {address_name}: {e}")

    def get_itinerary_transport(
            self,
            departure_coordinates: Point,
            arrival_coordinates: Point,
            travel_datetime: str | None,
            datetime_represents: str
        ) -> list[dict]:
        if travel_datetime:
            params = {
                'from': f"{departure_coordinates.x};{departure_coordinates.y}",
                'to': f"{arrival_coordinates.x};{arrival_coordinates.y}",
                'datetime': travel_datetime,
                'datetime_representss': datetime_represents,
                'allowed_id[]': ["commercial_mode:LocalTrain", "commercial_mode:RapidTransit"]
            }
        else:
            params = {
                'from': f"{departure_coordinates.x};{departure_coordinates.y}",
                'to': f"{arrival_coordinates.x};{arrival_coordinates.y}",
                'allowed_id[]': ["commercial_mode:LocalTrain", "commercial_mode:RapidTransit"]
            }
        r = self.session.get(f"{self.url_prim}/journeys", params=params)
        list_journeys = r.json().get("journeys")
        return list_journeys

    def get_itinerary_marche(self, departure_coordinates: Point, arrival_coordinates: Point) -> dict:
        params = {
            'from': f"{departure_coordinates.x};{departure_coordinates.y}",
            'to': f"{arrival_coordinates.x};{arrival_coordinates.y}",
        }
        r = self.session.get(f"{self.url_prim}/journeys", params=params)
        list_journeys = r.json().get("journeys")

        if len(list_journeys) == 1:
            return list_journeys[0]

        itinerary_marche = None

        for journey in list_journeys:
            if journey.get("type") == "non_pt_walk":
                itinerary_marche = journey
                break  # Prendre le premier trouvé

        if itinerary_marche is None:
            print("Aucun itinéraire de marche trouvé")
            return {}

        if len([j for j in list_journeys if j.get("type") == "non_pt_walk"]) > 1:
            print("Attention, il y a plus d'un itinéraire de marche trouvé - utilisation du premier")

        return itinerary_marche

    def get_itinerary_velo(
        self,
        departure_coordinates: Point,
        arrival_coordinates: Point,
        profile: str = "Default"
    ) -> list[dict]:
        body = {
            "waypoints": [
                {
                    "latitude": departure_coordinates.y,
                    "longitude": departure_coordinates.x
                },
                {
                    "latitude": arrival_coordinates.y,
                    "longitude": arrival_coordinates.x
                }
            ],
            "bikeDetails": {
                "profile": profile,
                "bikeType": "TRADITIONAL"
            }
        }

        # Paramètres de requête pour obtenir la géométrie
        params = {
            "instructions": "false",
            "elevations": "false",
            "geometry": "true",
            "single_result": "false",
            "bike_stations": "true",
            "objects_as_ids": "true",
            "merge_instructions": "false",
            "show_pushing_bike_instructions": "false"
        }

        r = self.session.post(f"{self.url_geovelo}/computedroutes",
                              data=json.dumps(body),
                              params=params)
        return r.json()
