"""
Configuration et constantes pour la génération d'itinéraires piétons.
"""

from pathlib import Path

# Chemins de base
# place le dossier de données à l'intérieur du package : itineraires_pietons/data
PACKAGE_DIR = Path(__file__).resolve().parent
DATA_DIR = PACKAGE_DIR / "data"
OUTPUT_DIR = DATA_DIR / "output"

# Fichiers d'entrée
POI_TYPES_FILE = DATA_DIR / "poi_types_relevant.txt"
DEFAULT_POI_PATH = DATA_DIR / "POI_IDF.csv"
DEFAULT_ARRETS_PATH = DATA_DIR / "referentiel_arret_derniere_version.parquet"

# Colonnes attendues
POI_COLUMNS = ["id", "nom_poi", "type_lieu", "source", "poi_lat", "poi_lon"]
ARRETS_COLUMNS = [
    "ArRId",
    "ArRName",
    "ArRLatitude",
    "ArRLongitude",
    "ArRType",
    "INSEE_COM",
    "nom_departement",
    "nom_epci",
    "nom_commune_standard",
]

# Filtres
TYPES_ARRETS = ["rail", "metro", "tram"]

# Paramètres spatiaux
MAX_DISTANCE = 500  # mètres
EARTH_RADIUS_M = 6371000.0  # rayon de la Terre en mètres

# Paramètres Valhalla
VALHALLA_PROFILE = "pedestrian"
VALHALLA_FORMAT = "geojson"
VALHALLA_RETRY_OVER_LIMIT = True


def load_poi_types():
    """Charge la liste des types de POI pertinents depuis le fichier de configuration."""
    if not POI_TYPES_FILE.exists():
        raise FileNotFoundError(f"Fichier des types POI introuvable : {POI_TYPES_FILE}")
    with open(POI_TYPES_FILE, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


# Chargement des types POI au démarrage
POI_TYPES = load_poi_types()
