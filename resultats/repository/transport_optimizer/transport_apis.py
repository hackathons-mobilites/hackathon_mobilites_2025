import requests
import pandas as pd
import polyline
import json
from shapely.geometry import LineString, mapping
from datetime import datetime
from config import GEOVELO_CONFIG, NAVITIA_CONFIG, DEFAULT_BIKE_CONFIG


class GeoveloClient:
    def __init__(self, api_key=None):
        self.api_key = api_key or GEOVELO_CONFIG["api_key"]
        self.base_url = GEOVELO_CONFIG["base_url"]
        self.default_params = GEOVELO_CONFIG["params"]

    def get_route(self, origin_coords, destination_coords, bike_config=None):
        """
        Calcule un itinéraire vélo entre deux points
        Returns:
            dict: {distance: float, duration: float, geometry: dict (GeoJSON)}
        """
        if bike_config is None:
            bike_config = DEFAULT_BIKE_CONFIG

        headers = GEOVELO_CONFIG["headers"].copy()
        headers["apikey"] = self.api_key

        # Construction du payload
        json_data = {
            "waypoints": [
                {
                    "latitude": origin_coords[1],
                    "longitude": origin_coords[0],
                    "title": "Start",
                },
                {
                    "latitude": destination_coords[1],
                    "longitude": destination_coords[0],
                    "title": "End",
                },
            ],
            "datetimeOfDeparture": datetime.now().isoformat(),
            "datetimeOfArrival": datetime.now().isoformat(),
            "bikeDetails": bike_config,
            "transportModes": ["BIKE"],
        }

        # Construction de l'URL avec paramètres
        url_params = "&".join([f"{k}={v}" for k, v in self.default_params.items()])
        url = f"{self.base_url}?{url_params}"

        try:
            response = requests.post(url, headers=headers, json=json_data)
            response.raise_for_status()

            json_resp = response.json()

            # Extraction des données de la première section
            geometry = json_resp[0]["sections"][0]["geometry"]
            distance = json_resp[0]["distances"]["total"]
            duration = json_resp[0]["duration"]

            # Décodage de la polyline (précision 6 pour Geovelo)
            decoded_polyline = polyline.decode(geometry, precision=6)
            coords_lonlat = [(lon, lat) for (lat, lon) in decoded_polyline]
            line_geometry = LineString(coords_lonlat)
            
            # Conversion en GeoJSON
            geojson_geometry = json.dumps(mapping(line_geometry), separators=(',', ':'))

            return {
                "distance": distance,
                "duration": duration // 60,  # Convertir en minutes
                "geometry": geojson_geometry,
            }

        except requests.exceptions.RequestException as e:
            print(f"Erreur API Geovelo: {e}")
            return None


class NavitiaClient:
    def __init__(self, base_url=None, api_key=None):
        self.base_url = base_url or NAVITIA_CONFIG["base_url"]
        self.api_key = api_key or NAVITIA_CONFIG["api_key"]
        self.headers = NAVITIA_CONFIG["headers"].copy()
        if self.api_key:
            self.headers["apikey"] = self.api_key

    def get_journey(self, origin_id, destination_id, datetime_str, max_duration=14400):
        """
        Calcule un itinéraire en transport en commun
        Returns:
            pd.Series: [ligne, duree_traj, heure_arrivee] ou Series vide
        """
        # Formatage des IDs Navitia
        ori_formatted = f"stop_point:IDFM:monomodalStopPlace:{origin_id}"
        dest_formatted = f"stop_point:IDFM:monomodalStopPlace:{destination_id}"

        # Construction de l'URL
        url = (
            f"{self.base_url}/journeys?"
            f"from={ori_formatted.replace(':', '%3A')}"
            f"&to={dest_formatted}"
            f"&datetime={datetime_str}"
            f"&max_duration={max_duration}"
            f"&datetime_represents=departure"
            f"&allowed_id%5B%5D=network%3AIDFM%3A71&allowed_id%5B%5D=network%3AIDFM%3A1046"
        )

        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()

            json_data = response.json()

            if "journeys" in pd.json_normalize(json_data).columns:
                tab_iti = self._parse_journeys(response)
                if len(tab_iti) > 0:
                    return tab_iti.loc[0, ["ligne", "duree_traj", "heure_arrivee", "geojson"]]

            return pd.Series()  # Retour vide en cas d'échec

        except requests.exceptions.RequestException as e:
            print(f"Erreur API Navitia: {e}")
            return pd.Series()

    def _parse_journeys(self, response):
        """Parse la réponse JSON de Navitia et extrait les informations d'itinéraire"""
        bdd = pd.json_normalize(response.json())["journeys"][0]
        df = pd.DataFrame(
            [],
            columns=["num_traj", "duree_traj1", "mode", "ligne", "deb_sec", "fin_sec", "geojson"],
        )
        nb_traj = len(bdd) if len(bdd) < 6 else 6

        for num_traj in range(nb_traj):
            traj = bdd[num_traj]
            duree_traj = traj["duration"]
            heure_arrivee = traj["arrival_date_time"]
            l_sec = []

            for s in traj["sections"]:
                if s["type"] == "public_transport":
                    mode = s["display_informations"]["commercial_mode"]
                    ligne = s["display_informations"]["label"]
                    dep = s["from"]["name"]
                    arr = s["to"]["name"]
                    # Récupérer le GeoJSON si disponible
                    geojson = s.get("geojson", None)
                    # Convertir le geojson dict en string JSON avec les bons guillemets
                    geojson_str = json.dumps(geojson, separators=(',', ':')) if geojson else None
                    l_sec.append(
                        [
                            num_traj,
                            round(duree_traj / 60),
                            heure_arrivee,
                            mode,
                            ligne,
                            dep,
                            arr,
                            geojson_str,
                        ]
                    )

            df = pd.concat(
                [
                    df,
                    pd.DataFrame(
                        l_sec,
                        columns=[
                            "num_traj",
                            "duree_traj",
                            "heure_arrivee",
                            "mode",
                            "ligne",
                            "deb_sec",
                            "fin_sec",
                            "geojson",
                        ],
                    ),
                ]
            )

        df_chaine = (
            df.groupby("num_traj")
            .agg(
                {
                    "ligne": lambda x: " > ".join(x),
                    "duree_traj": "first",
                    "heure_arrivee": "first",
                    "geojson": lambda x: [g for g in x if g is not None],  # Liste des geojson non-null
                }
            )
            .reset_index()
        )

        return df_chaine
