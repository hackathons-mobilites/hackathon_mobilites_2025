# Transport Optimizer

Package modulaire pour l'optimisation de trajets multimodaux (vélo + transport en commun).

## Architecture

```
transport_optimizer/
├── config.py              # Configuration et constantes API
├── data_loader.py          # Chargement des données gares  
├── spatial_service.py      # Services de géolocalisation et buffer
├── transport_apis.py       # Clients API (Navitia, Geovelo)
├── route_optimizer.py      # Logique d'optimisation des trajets
└── main.py                # Point d'entrée principal
```

## Utilisation

```python
from transport_optimizer import RouteOptimizer

# Configuration
optimizer = RouteOptimizer(
    parquet_path="data/emplacement-des-gares-idf.parquet",
    navitia_config={
        "base_url": "YOUR_NAVITIA_URL",
        "api_key": "YOUR_NAVITIA_KEY"
    }
)

# Trouver les itinéraires
routes = optimizer.find_optimal_routes(
    origin_coords=(2.301, 48.797),
    destination_coords=(1.743, 48.986), 
    buffer_radius=5000
)
```

## Fonctionnalités

- **Recherche spatiale** : Gares dans un rayon autour d'un point
- **API Geovelo** : Calcul d'itinéraires vélo pour rabattement/diffusion
- **API Navitia** : Calcul d'itinéraires transport en commun
- **Optimisation** : Combinaisons de tous les trajets possibles
- **Export** : Résultats en CSV avec géométries

## Configuration

Modifiez `config.py` pour vos clés API et paramètres.