"""
Constantes pour l'interface utilisateur de CycloFlow
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

# Descriptions simplifiées des codes météo (Météo Concept)
WEATHER_CODE_DESCRIPTIONS = {
    0: "Ensoleillé",
    1: "Peu nuageux",
    2: "Ciel voilé",
    3: "Nuageux",
    4: "Très nuageux",
    5: "Couvert",
    6: "Brouillard",
    7: "Brouillard givrant",
    10: "Pluie faible",
    11: "Pluie modérée",
    12: "Pluie forte",
    13: "Pluie très forte",
    14: "Pluie orageuse",
    15: "Neige faible",
    16: "Neige modérée",
    17: "Neige forte",
    18: "Neige très forte",
    19: "Pluie/neige mêlées faibles",
    20: "Pluie/neige mêlées modérées",
    21: "Pluie/neige mêlées fortes",
    22: "Pluie/neige mêlées très fortes",
    30: "Orage faible",
    31: "Orage modéré",
    32: "Orage fort",
    33: "Orage très fort",
    34: "Orage violent",
    40: "Bruine",
    41: "Neige et bruine",
    42: "Bruine verglaçante",
}

WEATHER_CODE_EMOJIS = {
    0: "☀️",
    1: "🌤️",
    2: "🌥️",
    3: "☁️",
    4: "☁️",
    5: "☁️",
    6: "🌫️",
    7: "❄️",
    10: "🌦️",
    11: "🌧️",
    12: "🌧️",
    13: "🌧️",
    14: "⛈️",
    15: "🌨️",
    16: "🌨️",
    17: "❄️",
    18: "❄️",
    19: "🌨️",
    20: "🌨️",
    21: "🌨️",
    22: "🌨️",
    30: "⛈️",
    31: "⛈️",
    32: "⛈️",
    33: "⛈️",
    34: "🌩️",
    40: "🌦️",
    41: "🌨️",
    42: "🌧️",
}
