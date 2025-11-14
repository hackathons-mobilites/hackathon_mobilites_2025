# 🚲🚇 Optimiseur d'Itinéraires Multimodaux

Système complet d'optimisation de trajets multimodaux (vélo + transport en commun) en Île-de-France avec interface web interactive.

## 🚀 Installation et démarrage rapide

1. **Installer les dépendances** :
```bash
pip install -r requirements.txt
```

2. **Vérifier les données** :
```
data/emplacement-des-gares-idf.parquet
```

3. **Lancer l'application web** :
```bash
streamlit run app.py
```

L'application s'ouvrira à `http://localhost:8501`

## 📁 Architecture du projet

```
transport_optimizer/
├── config.py              # Configuration et clés API
├── data_loader.py          # Chargement des données gares  
├── spatial_service.py      # Services géospatiaux et buffers
├── transport_apis.py       # Clients API (Navitia, Geovelo)
├── route_optimizer.py      # Logique d'optimisation des trajets
├── app.py                 # Interface Streamlit
├── main.py                # Script en ligne de commande
└── data/                  # Données des gares et résultats
```

## 🌐 Application Web Streamlit

### Fonctionnalités principales
- **📮 Géocodage d'adresses** : Recherche automatique des coordonnées
- **📅 Planification temporelle** : Sélection date et heure de départ
- **🔍 Rayon adaptatif** : Zone de recherche des gares (0.5-10 km)
- **🗺️ Visualisation interactive** : Cartes détaillées des itinéraires
- **💾 Export des données** : Téléchargement CSV complet

### Interface utilisateur
1. **Saisir les adresses** de départ et destination
2. **Géocoder automatiquement** avec les boutons 🔍
3. **Ajuster les paramètres** (date, heure, rayon)
4. **Calculer** avec le bouton 🚀 GO!
5. **Explorer les résultats** et visualiser sur carte

### Légende des tracés
- **🟢 Vert pointillé** : Trajet vélo de rabattement (origine → gare)
- **🔵 Bleu continu** : Transport en commun (gare → gare)
- **🔴 Rouge pointillé** : Trajet vélo de diffusion (gare → destination)

## 🐍 API Python

### Utilisation programmatique

```python
from route_optimizer import RouteOptimizer

# Configuration
optimizer = RouteOptimizer(
    parquet_path="data/emplacement-des-gares-idf.parquet"
)

# Trouver les itinéraires optimaux
routes = optimizer.find_optimal_routes(
    origin_coords=(2.301, 48.797),      # lon, lat
    destination_coords=(1.743, 48.986), # lon, lat
    buffer_radius=5000                   # mètres
)

print(f"{len(routes)} itinéraires trouvés")
print(routes[['nom_gares_ori', 'nom_gares_dest', 'duree_totale_parcours']])
```

### Script en ligne de commande

```bash
python main.py
```

## 🔧 Fonctionnalités techniques

### Optimisations de performance
- **Cache des trajets vélo** : Évite les appels API redondants
- **Calculs parallélisés** : Améliore les temps de réponse
- **Gestion intelligente des erreurs** : Robustesse des API externes

### Services géospatiaux
- **Recherche spatiale** : Gares dans un rayon configurable
- **Projections cartographiques** : Lambert-93 pour précision métrique
- **Geometries GeoJSON** : Visualisation web complète

### APIs intégrées
- **🚲 Geovelo** : Itinéraires vélo optimisés
- **🚇 Navitia** : Transport en commun temps réel
- **🗺️ Nominatim** : Géocodage d'adresses

## ⚙️ Configuration

Modifiez `config.py` pour vos paramètres :

```python
# Clés API
GEOVELO_CONFIG = {
    "api_key": "VOTRE_CLE_GEOVELO"
}

NAVITIA_CONFIG = {
    "api_key": "VOTRE_CLE_NAVITIA"
}

# Paramètres par défaut
DEFAULT_JOURNEY_CONFIG = {
    "datetime_str": "20251114T120000",
    "max_duration": 14400  # 4 heures
}
```

## 🔍 Données de sortie

### Colonnes principales
- **Gares** : `nom_gares_ori`, `nom_gares_dest`, `mode_ori`, `mode_dest`
- **Trajets vélo** : `rabattement_distance`, `diffusion_distance`, `distance_velo_totale`
- **Temps** : `duree_velo_totale`, `duree_traj`, `duree_totale_parcours`
- **Transport** : `ligne`, informations détaillées des correspondances
- **Géométries** : GeoJSON pour visualisation cartographique

## 🛠️ Dépannage

### Erreurs courantes
- **Géocodage échoué** : Vérifiez la syntaxe des adresses
- **Aucun itinéraire** : Augmentez le rayon de recherche
- **Timeout API** : Patientez ou relancez le calcul

### Performance
- Rayon optimal : 2-5 km pour équilibre rapidité/couverture
- Temps de calcul : 30-60 secondes selon les combinaisons
- Connexion internet requise pour les cartes

## 📊 Exemples de résultats

```csv
nom_gares_ori,nom_gares_dest,distance_velo_totale,duree_totale_parcours,ligne
Bagneux,Limay,3245,67,"RER C"
La Défense,Élancourt,2890,72,"RER A, Transilien N"
```