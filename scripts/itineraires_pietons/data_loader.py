"""
Services de chargement et préparation des données (Data Layer).
"""

import logging
import pandas as pd
from typing import Tuple

from .config import (
    POI_COLUMNS,
    ARRETS_COLUMNS,
    POI_TYPES,
    TYPES_ARRETS,
    DEFAULT_POI_PATH,
    DEFAULT_ARRETS_PATH,
)

logger = logging.getLogger(__name__)


class DataLoader:
    """Chargeur de données pour les POI et arrêts."""

    @staticmethod
    def load_poi(poi_path: str = None) -> pd.DataFrame:
        """
        Charge et nettoie les données POI.

        Args:
            poi_path: chemin vers le fichier CSV des POI (optionnel)

        Returns:
            DataFrame des POI nettoyés et filtrés
        """
        path = poi_path or str(DEFAULT_POI_PATH)
        logger.info(f"Chargement des POIs depuis {path}")

        df_poi = pd.read_csv(path, usecols=POI_COLUMNS)
        df_poi.dropna(subset=["id"], inplace=True)

        # Suppression des doublons exacts
        before = len(df_poi)
        df_poi = df_poi.drop_duplicates(subset=["poi_lat", "poi_lon", "nom_poi"])
        after = len(df_poi)
        if after < before:
            logger.info(f"Supprimé {before - after} lignes POI dupliquées")

        # Filtrage par types pertinents
        df_poi = df_poi[df_poi["type_lieu"].isin(POI_TYPES)]
        logger.info(f"{len(df_poi)} POIs après filtrage par types pertinents")

        return df_poi

    @staticmethod
    def load_arrets(arrets_path: str = None) -> pd.DataFrame:
        """
        Charge et filtre les données d'arrêts.

        Args:
            arrets_path: chemin vers le fichier parquet des arrêts (optionnel)

        Returns:
            DataFrame des arrêts filtrés
        """
        path = arrets_path or str(DEFAULT_ARRETS_PATH)
        logger.info(f"Chargement des arrêts depuis {path}")

        df_arrets = pd.read_parquet(path, columns=ARRETS_COLUMNS)

        # Filtrage par types d'arrêts
        df_arrets = df_arrets[df_arrets["ArRType"].isin(TYPES_ARRETS)]
        logger.info(f"{len(df_arrets)} arrêts après filtrage par type {TYPES_ARRETS}")

        return df_arrets

    @staticmethod
    def load_data(
        poi_path: str = None, arrets_path: str = None
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Charge à la fois les POI et les arrêts.

        Args:
            poi_path: chemin vers le fichier CSV des POI
            arrets_path: chemin vers le fichier parquet des arrêts

        Returns:
            Tuple (DataFrame POI, DataFrame arrêts)
        """
        df_poi = DataLoader.load_poi(poi_path)
        df_arrets = DataLoader.load_arrets(arrets_path)
        return df_poi, df_arrets
