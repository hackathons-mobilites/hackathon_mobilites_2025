"""
Orchestrateur principal - coordonne les différents services (Application Layer).
"""

import random
import logging
from pathlib import Path
from typing import Optional
from tqdm import tqdm

from .data_loader import DataLoader
from .spatial_service import SpatialService
from .routing_service import RoutingService
from .export_service import ExportService
from .config import OUTPUT_DIR, MAX_DISTANCE

logger = logging.getLogger(__name__)


class ItineraryOrchestrator:
    """Orchestre la génération complète des itinéraires piétons."""

    def __init__(self, valhalla_url: Optional[str] = None):
        """
        Initialise l'orchestrateur.

        Args:
            valhalla_url: URL du serveur Valhalla (optionnel)
        """
        self.routing_service = RoutingService(valhalla_url)
        self.spatial_service = SpatialService()
        self.export_service = ExportService()

    def generate_itineraries(
        self,
        poi_path: Optional[str] = None,
        arrets_path: Optional[str] = None,
        output_folder: Optional[Path] = None,
        max_distance: float = MAX_DISTANCE,
        limit: Optional[int] = None,
        communes: Optional[list] = None,
    ) -> int:
        """
        Pipeline complet de génération des itinéraires.

        Args:
            poi_path: chemin vers le fichier POI
            arrets_path: chemin vers le fichier arrêts
            output_folder: dossier de sortie
            max_distance: rayon de recherche (m)
            limit: limite du nombre d'itinéraires à générer (pour tests)
            communes: liste de codes INSEE de communes à filtrer (optionnel)

        Returns:
            Nombre d'itinéraires générés
        """
        logger.info("=== Démarrage de la génération des itinéraires ===")

        # 1. Chargement des données
        df_poi, df_arrets = DataLoader.load_data(poi_path, arrets_path)

        # 1b. Filtrage par communes si spécifié
        if communes:
            logger.info(f"Filtrage des arrêts pour les communes: {communes}")
            # Convertir INSEE_COM en string pour la comparaison
            df_arrets["INSEE_COM"] = df_arrets["INSEE_COM"].astype(str)
            communes_str = [str(c) for c in communes]
            df_arrets = df_arrets[df_arrets["INSEE_COM"].isin(communes_str)]
            logger.info(f"{len(df_arrets)} arrêts après filtrage par communes")

            if len(df_arrets) == 0:
                logger.warning(f"Aucun arrêt trouvé pour les communes: {communes}")
                return 0

        # 2. Recherche spatiale
        pairs = self.spatial_service.find_nearby_pois(df_arrets, df_poi, max_distance)

        if not pairs:
            logger.warning("Aucune paire arrêt-POI trouvée dans le rayon spécifié")
            return 0

        # 3. Génération des itinéraires
        output_folder = output_folder or OUTPUT_DIR
        pairs_to_process = random.sample(pairs, limit) if limit else pairs

        generated_count = 0
        for arret_id, poi_id, distance in tqdm(
            pairs_to_process, desc="Calcul des itinéraires"
        ):
            try:
                arret = df_arrets[df_arrets["ArRId"] == arret_id].iloc[0]
                poi = df_poi[df_poi["id"] == poi_id].iloc[0]

                # Coordonnées pour Valhalla (lon, lat)
                origin = (arret["ArRLongitude"], arret["ArRLatitude"])
                destination = (poi["poi_lon"], poi["poi_lat"])

                # Calcul de l'itinéraire
                route = self.routing_service.calculate_route(origin, destination)
                if route is None:
                    continue

                # Création de la feature GeoJSON
                feature = self.export_service.create_geojson_feature(
                    route, arret, poi, distance
                )

                # Génération du nom de fichier et sauvegarde
                filename = self.export_service.generate_filename(arret, poi)
                self.export_service.save_geojson(feature, filename, output_folder)

                generated_count += 1

            except Exception as e:
                logger.error(
                    f"Erreur lors du traitement de la paire {arret_id}-{poi_id}: {e}"
                )
                continue

        logger.info(
            f"=== Génération terminée : {generated_count} itinéraires sauvegardés dans {output_folder} ==="
        )
        return generated_count
