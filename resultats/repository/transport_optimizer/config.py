import logging

# API Geovelo
GEOVELO_CONFIG = {
    "base_url": "https://prim.iledefrance-mobilites.fr/marketplace/computedroutes",
    "api_key": "GQP6YxRWmagxg9GIFL8oLIeMPpxnMtpP",
    "headers": {
        "Accept": "application/json", 
        "Content-Type": "application/json"
    },
    "params": {
        "instructions": "false",
        "elevations": "false", 
        "geometry": "true",
        "single_result": "true",
        "bike_stations": "false",
        "objects_as_ids": "true",
        "merge_instructions": "false",
        "show_pushing_bike_instructions": "false"
    }
}

# Configuration Navitia
NAVITIA_CONFIG = {
    "base_url": "https://prim.iledefrance-mobilites.fr/marketplace/v2/navitia",
    "api_key": "RIpBwKRzsMAwQAPN2ttH4iE9ISQ7dcEz",
    "headers": {
        "Accept": "application/json"
    }
}

# Configuration spatiale
SPATIAL_CONFIG = {
    "source_crs": "EPSG:4326",  # WGS84
    "projected_crs": "EPSG:2154",  # RGF93 / Lambert-93
    "default_buffer_radius": 2000,  # mètres
    "transport_modes": ["TRAIN", "RER"]
}

# Configuration vélo par défaut
DEFAULT_BIKE_CONFIG = {
    "profile": "EXPERT",
    "bikeType": "TRADITIONAL", 
    "averageSpeed": 16,
    "eBike": False,
    "bikeStations": [{"from": 0, "to": 0}]
}

# Configuration par défaut pour les itinéraires
DEFAULT_JOURNEY_CONFIG = {
    "datetime_str": "20251114T120000",  # Format Navitia: AAAAMMJJTHHMISS
    "max_duration": 14400  # 4 heures en secondes
}

# Configuration du logger
def setup_logger(name="transport_optimizer", level=logging.INFO):
    """Configure et retourne un logger pour l'application"""
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(level)
    
    return logger