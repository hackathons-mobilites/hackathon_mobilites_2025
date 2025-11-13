"""
Constantes pour l'interface utilisateur de Vel'Octo
"""

# Configuration DEBUG (à supprimer plus tard)
DEBUG_ADDRESSES = {
    "departure": "14 Rue du Prévôt, Paris, France",
    "arrival": "34 Avenue des Champs-Élysées, Paris, France"
}

# Constantes géographiques
PARIS_CENTER = (48.8566, 2.3522)
DEFAULT_USER_LOCATION = (48.8580848, 2.3861367)  # Pan Piper

# Couleurs des routes
ROUTE_COLORS = {
    'RECOMMENDED': '#2E86AB',  # Bleu
    'SAFER': '#A23B72',       # Rose
    'FASTER': '#F18F01'       # Orange
}

# Styles de carte disponibles
MAP_STYLES = [
    'OpenStreetMap',
    'CartoDB positron',
    'CartoDB dark_matter',
    'Esri WorldImagery',
    'Esri WorldTopoMap',
    'Esri NatGeoWorldMap'
]

# URLs des cartes Esri
ESRI_URLS = {
    'Esri WorldImagery': ('https://server.arcgisonline.com/ArcGIS/rest/services/'
                          'World_Imagery/MapServer/tile/{z}/{y}/{x}'),
    'Esri WorldTopoMap': ('https://server.arcgisonline.com/ArcGIS/rest/services/'
                          'World_Topo_Map/MapServer/tile/{z}/{y}/{x}'),
    'Esri NatGeoWorldMap': ('https://server.arcgisonline.com/ArcGIS/rest/services/'
                            'NatGeo_World_Map/MapServer/tile/{z}/{y}/{x}')
}

# Attributions simplifiées des cartes
ATTR_MAP = {
    'OpenStreetMap': 'OSM',
    'CartoDB positron': 'CARTO',
    'CartoDB dark_matter': 'CARTO'
}
