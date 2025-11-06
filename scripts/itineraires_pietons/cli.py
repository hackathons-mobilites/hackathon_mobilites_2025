"""
Point d'entrée CLI pour la génération d'itinéraires piétons.
"""

import argparse
import logging
import sys
from pathlib import Path

from .orchestrator import ItineraryOrchestrator
from .config import DEFAULT_POI_PATH, DEFAULT_ARRETS_PATH, OUTPUT_DIR, MAX_DISTANCE


def setup_logging(verbose: bool = False):
    """Configure le système de logging."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )


def main():
    """Point d'entrée principal du CLI."""
    parser = argparse.ArgumentParser(
        description="Génération d'itinéraires piétons entre arrêts et POI"
    )

    parser.add_argument(
        "--poi",
        type=str,
        default=str(DEFAULT_POI_PATH),
        help=f"Chemin vers le fichier CSV des POI (défaut: {DEFAULT_POI_PATH})",
    )

    parser.add_argument(
        "--arrets",
        type=str,
        default=str(DEFAULT_ARRETS_PATH),
        help=f"Chemin vers le fichier parquet des arrêts (défaut: {DEFAULT_ARRETS_PATH})",
    )

    parser.add_argument(
        "--output",
        type=str,
        default=str(OUTPUT_DIR),
        help=f"Dossier de sortie pour les GeoJSON (défaut: {OUTPUT_DIR})",
    )

    parser.add_argument(
        "--distance",
        type=float,
        default=MAX_DISTANCE,
        help=f"Rayon de recherche en mètres (défaut: {MAX_DISTANCE})",
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Limite du nombre d'itinéraires à générer (pour tests)",
    )

    parser.add_argument(
        "--communes",
        type=str,
        nargs="+",
        default=None,
        help="Filtrer par code(s) INSEE de commune(s) (ex: 75056 pour Paris, 92050 pour Nanterre)",
    )

    parser.add_argument(
        "--valhalla-url",
        type=str,
        default=None,
        help="URL du serveur Valhalla (optionnel)",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Active le mode verbeux (DEBUG)",
    )

    args = parser.parse_args()

    # Configuration du logging
    setup_logging(args.verbose)

    # Création de l'orchestrateur
    orchestrator = ItineraryOrchestrator(valhalla_url=args.valhalla_url)

    # Génération des itinéraires
    try:
        count = orchestrator.generate_itineraries(
            poi_path=args.poi,
            arrets_path=args.arrets,
            output_folder=Path(args.output),
            max_distance=args.distance,
            limit=args.limit,
            communes=args.communes,
        )
        print(f"\n✓ {count} itinéraires générés avec succès")
        return 0
    except Exception as e:
        logging.error(f"Erreur fatale: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
