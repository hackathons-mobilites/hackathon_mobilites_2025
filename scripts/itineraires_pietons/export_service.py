"""
Service d'export des itinéraires en GeoJSON (Business Logic Layer).
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any
import pandas as pd

from .config import OUTPUT_DIR

logger = logging.getLogger(__name__)


class ExportService:
    """Service d'export des itinéraires calculés."""

    @staticmethod
    def create_geojson_feature(
        route_obj, arret: pd.Series, poi: pd.Series, distance: float
    ) -> Dict[str, Any]:
        """
        Crée une Feature GeoJSON à partir d'un itinéraire calculé.

        Args:
            route_obj: objet route retourné par Valhalla
            arret: Series pandas de l'arrêt
            poi: Series pandas du POI
            distance: distance à vol d'oiseau (m)

        Returns:
            Dictionnaire représentant une Feature GeoJSON
        """
        geometry = {"type": "LineString", "coordinates": route_obj.geometry}

        distance_reelle = getattr(route_obj, "distance", 0)
        time_seconds = getattr(route_obj, "time", 0)

        properties = {
            "arret_id": str(arret["ArRId"]),
            "arret_nom": arret.get("ArRName", ""),
            "arret_type": arret["ArRType"],
            "poi_id": str(poi["id"]),
            "poi_nom": poi.get("nom_poi", ""),
            "poi_type": poi["type_lieu"],
            "distance_vol_oiseau": round(distance, 2),
            "distance_reelle": round(distance_reelle, 2),
            "duree_marche": round(time_seconds / 60, 2),
            "code_insee": str(arret["INSEE_COM"]),
            "commune": arret["nom_commune_standard"],
            "epci": arret["nom_epci"],
            "departement": arret["nom_departement"],
        }

        return {"type": "Feature", "geometry": geometry, "properties": properties}

    @staticmethod
    def generate_filename(arret: pd.Series, poi: pd.Series) -> str:
        """
        Génère un nom de fichier stable pour l'itinéraire.

        Args:
            arret: Series pandas de l'arrêt
            poi: Series pandas du POI

        Returns:
            Nom de fichier (sans chemin)
        """
        code_insee = str(arret.get("INSEE_COM", "unknown_insee")).strip()
        nom_arret = (
            str(arret.get("ArRName", arret.get("ArRId"))).strip().replace(" ", "_")
        )
        poi_id = str(poi["id"]).strip().replace("/", "_").replace("\\", "_")

        return f"{code_insee}_{nom_arret}_{poi_id}.geojson"

    @staticmethod
    def save_geojson(
        feature: Dict[str, Any], filename: str, output_folder: Path = OUTPUT_DIR
    ) -> Path:
        """
        Sauvegarde une Feature GeoJSON dans un fichier.

        Args:
            feature: Feature GeoJSON à sauvegarder
            filename: nom du fichier de sortie
            output_folder: dossier de sortie

        Returns:
            Path du fichier créé
        """
        output_folder = Path(output_folder)
        output_folder.mkdir(parents=True, exist_ok=True)

        geojson = {"type": "FeatureCollection", "features": [feature]}
        output_file = output_folder / filename

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(geojson, f, ensure_ascii=False, indent=2)

        return output_file
