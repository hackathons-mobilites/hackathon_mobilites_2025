import json
from urllib.parse import urljoin
from shapely.geometry import Point

import requests

from config.var_env import API_KEY_PRIM, BASE_URL_PRIM, PATH_GEOVELO, PATH_CALCULATEUR_IDFM
from src.itineraire.domain.ports.source_handler import SourceHandler

class ApiHandler(SourceHandler):
    def __init__(self):
        self.url_prim = urljoin(BASE_URL_PRIM, PATH_CALCULATEUR_IDFM)

        self.url_geovelo = urljoin(BASE_URL_PRIM, PATH_GEOVELO)

        self.headers = {'apiKey': API_KEY_PRIM}
        self.session = requests.Session()

        self.session.headers.update(self.headers)

    def get_address_coordinates(self, address_name: str) -> Point:
        params = {'q': address_name}
        r = self.session.get(f"{self.url_prim}/places", params=params)
        coordinates = r.json().get('places')[0].get('id').split(";")
        return Point(coordinates[0], coordinates[1])
    
    def get_itinerary_transport(self, departure_coordinates: Point, arrival_coordinates: Point) -> dict:
        params = {
            'from': f"{departure_coordinates.x};{departure_coordinates.y}",
            'to': f"{arrival_coordinates.x};{arrival_coordinates.y}",
        }
        r = self.session.get(f"{self.url_prim}/journeys", params=params)
        return r.json()
    
    def get_itinerary_marche(self, departure_coordinates: Point, arrival_coordinates: Point) -> dict:
        params = {
            'from': f"{departure_coordinates.x};{departure_coordinates.y}",
            'to': f"{arrival_coordinates.x};{arrival_coordinates.y}",
        }
        r = self.session.get(f"{self.url_prim}/journeys", params=params)
        return r.json()
    
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
            ]
            ,
            "bikeDetails":{
                "profile": profile,
                "bikeType": "TRADITIONAL"
            }
        }
        r = self.session.post(f"{self.url_geovelo}/computedroutes", data=json.dumps(body))
        return r.json()