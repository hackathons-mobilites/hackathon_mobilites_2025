"""
Service de calcul d'itinéraires via Valhalla (Business Logic Layer).
"""

import logging
from routingpy import Valhalla
from typing import Optional

from .config import (
    VALHALLA_PROFILE,
    VALHALLA_FORMAT,
    VALHALLA_RETRY_OVER_LIMIT,
)

logger = logging.getLogger(__name__)


class RoutingService:
    """Service de calcul d'itinéraires piétons via Valhalla."""

    def __init__(self, valhalla_url: Optional[str] = None):
        """
        Initialise le service de routing.

        Args:
            valhalla_url: URL du serveur Valhalla (optionnel, utilise le défaut si None)
        """
        if valhalla_url:
            self.client = Valhalla(
                base_url=valhalla_url, retry_over_query_limit=VALHALLA_RETRY_OVER_LIMIT
            )
        else:
            self.client = Valhalla(retry_over_query_limit=VALHALLA_RETRY_OVER_LIMIT)
        logger.info("Service de routing Valhalla initialisé")

    def calculate_route(self, origin: tuple, destination: tuple):
        """
        Calcule un itinéraire piéton entre deux points.

        Args:
            origin: tuple (lon, lat) du point d'origine
            destination: tuple (lon, lat) du point de destination

        Returns:
            Objet route de routingpy, ou None si erreur
        """
        try:
            route = self.client.directions(
                locations=[origin, destination],
                profile=VALHALLA_PROFILE,
                format=VALHALLA_FORMAT,
            )
            return route
        except Exception as e:
            logger.error(
                f"Erreur lors du calcul d'itinéraire {origin} -> {destination}: {e}"
            )
            return None
