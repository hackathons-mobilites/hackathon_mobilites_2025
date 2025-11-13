# Application Streamlit - Optimiseur d'Itinéraires Multimodaux

Cette application Streamlit permet de calculer et visualiser des itinéraires multimodaux (vélo + transport en commun) en Île-de-France de manière interactive.

## Installation

1. Installer les dépendances :
```bash
pip install -r requirements_streamlit.txt
```

2. Vérifier que vous avez bien le fichier de données des gares :
```
data/emplacement-des-gares-idf.parquet
```

## Lancement de l'application

```bash
streamlit run app.py
```

L'application s'ouvrira automatiquement dans votre navigateur à l'adresse `http://localhost:8501`

## Fonctionnalités

### 📍 Sélection des coordonnées
- Cliquez sur la carte interactive dans la barre latérale
- Utilisez les boutons "Définir comme origine" et "Définir comme destination"
- Les coordonnées par défaut sont Bagneux → Limay

### 📅 Date et heure
- Sélecteur de date (jusqu'à 30 jours dans le futur)
- Sélecteur d'heure précis

### 🔍 Rayon de recherche
- Curseur de 0,5 à 10 km
- Détermine la zone de recherche des gares autour des points choisis

### 🚀 Calcul et résultats
- Bouton "GO!" pour lancer le calcul
- Affichage des statistiques générales
- Tableau des itinéraires triés par temps total
- Sélection d'un itinéraire pour visualisation détaillée

### 🗺️ Visualisation des trajets
- **Rouge pointillé** : Trajet vélo de rabattement (origine → gare)
- **Bleu continu** : Transport en commun (gare → gare)
- **Turquoise pointillé** : Trajet vélo de diffusion (gare → destination)
- Marqueurs verts/rouges pour les gares de départ/arrivée

### 💾 Export des données
- Téléchargement des résultats complets en CSV
- Nom de fichier automatique avec date/heure

## Structure des données

L'application utilise les données générées par `main.py` avec les colonnes suivantes :
- Informations des gares (nom, coordonnées, modes)
- Distances et durées des trajets vélo
- Lignes et horaires des transports en commun
- Géométries GeoJSON pour la visualisation
- Totaux calculés (distance_velo_totale, duree_totale_parcours)

## Dépannage

### Erreur de parsing GeoJSON
Si vous voyez des erreurs de parsing, vérifiez que les données CSV sont bien générées avec les corrections de format JSON (guillemets doubles).

### Performance
Pour de meilleures performances :
- Utilisez un rayon de recherche raisonnable (2-5 km)
- Les calculs peuvent prendre 30-60 secondes selon le nombre de combinaisons

### Carte vide
Si la carte ne s'affiche pas :
- Vérifiez votre connexion internet (Folium utilise des tuiles en ligne)
- Redémarrez l'application Streamlit

## Configuration

Les paramètres par défaut peuvent être modifiés dans :
- `config.py` : Configuration générale, clés API
- `app.py` : Coordonnées par défaut, styles de carte

## APIs utilisées

- **Geovelo** : Calcul des itinéraires vélo
- **Navitia** : Calcul des itinéraires transport en commun
- **OpenStreetMap** : Tuiles de carte (via Folium)