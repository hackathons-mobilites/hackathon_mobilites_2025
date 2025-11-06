# Itinéraires piétons — Architecture modulaire

Ce package génère des itinéraires piétons entre arrêts de transport (rail/metro/tram) et points d'intérêt (POI) proches.

## Architecture

Le code suit une **architecture en couches (Layered Architecture)** qui sépare clairement les responsabilités :

```
itineraires_pietons/
├── __init__.py          # Package root
├── __main__.py          # Point d'entrée module
├── cli.py               # Interface CLI (Presentation Layer)
├── orchestrator.py      # Orchestration (Application Layer)
├── config.py            # Configuration et constantes
├── data_loader.py       # Chargement données (Data Layer)
├── spatial_service.py   # Recherche spatiale (Business Logic)
├── routing_service.py   # Calcul itinéraires (Business Logic)
└── export_service.py    # Export GeoJSON (Business Logic)
```

## Utilisation

### Installation des dépendances

```powershell
pip install -r requirements.txt
```

### Exécution basique

```powershell
# Depuis le dossier 'scripts'
python -m itineraires_pietons

# Ou avec options
python -m itineraires_pietons --limit 10 --verbose
```

### Options CLI

```powershell
python -m itineraires_pietons --help

Options:
  --poi PATH              Fichier CSV des POI
  --arrets PATH           Fichier parquet des arrêts
  --output PATH           Dossier de sortie
  --distance METERS       Rayon de recherche (défaut: 500m)
  --limit N               Limiter à N itinéraires (tests)
  --communes CODE [CODE ...] Filtrer par code(s) INSEE (ex: 75056 92050)
  --valhalla-url URL      URL serveur Valhalla
  -v, --verbose           Mode debug
```

### Exemples d'utilisation

```powershell
# Générer des itinéraires uniquement pour Paris (75056)
python -m itineraires_pietons --communes 75056

# Générer pour plusieurs communes (Paris et Nanterre)
python -m itineraires_pietons --communes 75056 92050

# Combiner avec d'autres filtres
python -m itineraires_pietons --communes 75056 --distance 300 --limit 20 -v
```

⚠️ Il est aussi possible de restreindre ou de changer les types de POI considérés via le fichier *poi_types_relevant.txt*.
Pour ce faire choisissez les POI qui vous sont pertinents dans le fichier *all_poi_types.txt* et reportez-les dans le fichier *relevant*.
Ainsi vous pouvez par exemple générer uniquement les tracés des gares vers les boulangeries de la commune de Versailles (78000).

## Scripts utilitaires

### unify_geojsons.py

Script utilitaire pour agréger plusieurs fichiers GeoJSON en un seul fichier unifié. Utile pour consolider les itinéraires générés par commune ou par zone géographique.

```powershell
python unify_geojsons.py
```

Ce script parcourt les fichiers GeoJSON de sortie et les combine en une seule FeatureCollection, facilitant ainsi l'analyse globale et la visualisation cartographique des données.
