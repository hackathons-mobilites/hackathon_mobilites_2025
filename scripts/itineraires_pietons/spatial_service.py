"""
Service de recherche spatiale et calculs de distance (Business Logic Layer).
"""

import logging
import numpy as np
import pandas as pd
from scipy.spatial import cKDTree
from typing import List, Tuple

from .config import MAX_DISTANCE, EARTH_RADIUS_M

logger = logging.getLogger(__name__)


class SpatialService:
    """Service pour les opérations spatiales (recherche de voisins, calculs de distances)."""

    @staticmethod
    def haversine_vectorized(
        lat0: float, lon0: float, lats: np.ndarray, lons: np.ndarray
    ) -> np.ndarray:
        """
        Calcul vectorisé de la distance haversine entre un point et un tableau de points.

        Args:
            lat0, lon0: coordonnées du point d'origine (degrés)
            lats, lons: tableaux numpy des coordonnées de destination (degrés)

        Returns:
            Tableau numpy des distances en mètres
        """
        lat0_rad, lon0_rad = np.radians(lat0), np.radians(lon0)
        lats_rad = np.radians(lats)
        lons_rad = np.radians(lons)

        dlat = lats_rad - lat0_rad
        dlon = lons_rad - lon0_rad
        a = (
            np.sin(dlat / 2.0) ** 2
            + np.cos(lat0_rad) * np.cos(lats_rad) * np.sin(dlon / 2.0) ** 2
        )
        c = 2 * np.arcsin(np.sqrt(a))
        return EARTH_RADIUS_M * c

    @staticmethod
    def find_nearby_pois(
        df_arrets: pd.DataFrame,
        df_poi: pd.DataFrame,
        max_distance: float = MAX_DISTANCE,
    ) -> List[Tuple[str, str, float]]:
        """
        Trouve les paires (arrêt, POI) dans un rayon donné en utilisant KDTree.

        Args:
            df_arrets: DataFrame des arrêts
            df_poi: DataFrame des POI
            max_distance: rayon de recherche en mètres

        Returns:
            Liste de tuples (arret_id, poi_id, distance_m)
        """
        logger.info(
            f"Recherche des POIs dans un rayon de {max_distance}m autour des arrêts"
        )

        # Conversion des coordonnées en radians pour KDTree
        coords_arrets = np.radians(
            df_arrets[["ArRLongitude", "ArRLatitude"]].to_numpy()
        )
        coords_poi = np.radians(df_poi[["poi_lon", "poi_lat"]].to_numpy())

        tree = cKDTree(coords_poi)

        # Conversion de la distance en radians (approximation)
        max_distance_rad = max_distance / 111000.0

        # Requête batch sur tous les arrêts
        neighbours_list = tree.query_ball_point(coords_arrets, r=max_distance_rad)

        # Extraction des arrays pour accès rapide
        poi_lat_arr = df_poi["poi_lat"].to_numpy()
        poi_lon_arr = df_poi["poi_lon"].to_numpy()
        poi_uid_arr = df_poi.get("poi_uid", df_poi.get("id")).to_numpy()

        arret_ids = df_arrets["ArRId"].to_numpy()
        arret_lat_arr = df_arrets["ArRLatitude"].to_numpy()
        arret_lon_arr = df_arrets["ArRLongitude"].to_numpy()

        pairs = []

        # Traitement vectorisé par arrêt
        for i, nbrs in enumerate(neighbours_list):
            if not nbrs:
                continue

            lat0 = arret_lat_arr[i]
            lon0 = arret_lon_arr[i]

            # Coords des POI voisins
            sel_poi_lats = poi_lat_arr[nbrs]
            sel_poi_lons = poi_lon_arr[nbrs]

            # Distances haversine vectorisées
            dists = SpatialService.haversine_vectorized(
                lat0, lon0, sel_poi_lats, sel_poi_lons
            )

            # Filtrage par distance max
            mask = dists <= max_distance
            if not np.any(mask):
                continue

            sel_indices = np.array(nbrs)[mask]
            sel_dists = dists[mask]
            sel_poi_uids = poi_uid_arr[sel_indices]

            # Ajout des paires
            arret_id = arret_ids[i]
            pairs.extend(
                zip(
                    [arret_id] * len(sel_poi_uids),
                    sel_poi_uids.tolist(),
                    sel_dists.tolist(),
                )
            )

        logger.info(f"Trouvé {len(pairs)} paires arrêt-POI dans le rayon spécifié")
        return pairs
