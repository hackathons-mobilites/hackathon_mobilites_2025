import streamlit as st
import folium
from streamlit_folium import st_folium
from src.parking_velo.domain.apps.get_parking_velo import get_parking_velo
from src.parking_velo.config.filters import ParkingVeloFilters
from folium.plugins import MarkerCluster
import json
import polyline

# Configuration de la page
st.set_page_config(page_title="Vel'Octo", page_icon="🚴", layout="centered")

# Titre de la page
st.title("Bienvenue sur l'application Vel'Octo")

# Contenu de la page
st.write("""
### Page d'accueil

Cette application est un exemple simple utilisant Streamlit.

- Utilisez le menu à gauche pour naviguer.
- Ajoutez vos fonctionnalités ici.

Bonne exploration !
""")

user_lat, user_lon = 48.8580848, 2.3861367  # Pan Piper

# Centrer la carte sur la position par défaut
m = folium.Map(location=[user_lat, user_lon], zoom_start=12)
folium.Marker(
    location=[user_lat, user_lon],
    popup="Vous êtes ici",
    icon=folium.Icon(color='red', icon='user', prefix='fa')
).add_to(m)

# Ajouter un cluster pour les autres marqueurs
marker_cluster = MarkerCluster().add_to(m)

# Récupérer les données des parkings vélo
st.write("## Parkings vélo à Paris")

try:
    # Appel de la fonction pour obtenir les données filtrées
    @st.cache_data
    def load_parking_data():
        return get_parking_velo(filter=ParkingVeloFilters.privee_abris)

    parking_data = load_parking_data()

    # Ajouter les points des parkings sur la carte
    for _, row in parking_data.iterrows():
        folium.Marker(
            location=[row.geometry.y, row.geometry.x],
            popup=f"Parking ID: {row.get('osm_id', 'N/A')}<br>Capacité: {row.get('capacite', 'N/A')}",
            icon=folium.Icon(color='green', icon='bicycle', prefix='fa')
        ).add_to(marker_cluster)

    # Charger la réponse de l'API
    with open("response_example.json", "r") as file:
        api_response = json.load(file)

    # Extraire le chemin recommandé
    recommended_section = next(
        (section for route in api_response for section in route["sections"] if route["title"] == "RECOMMENDED"),
        None
    )

    # Vérifier si la section recommandée est trouvée
    if recommended_section:
        encoded_geometry = recommended_section["geometry"]

        try:
            decoded_path = polyline.decode(encoded_geometry, precision=6)

            # Ajouter le chemin recommandé à la carte
            folium.PolyLine(
                locations=decoded_path,
                color="blue",
                weight=5,
                opacity=0.8
            ).add_to(m)
        except Exception as decode_error:
            st.error(f"Erreur lors du décodage de la géométrie : {decode_error}")
    else:
        st.warning("Aucune section recommandée trouvée dans la réponse de l'API.")

    # Afficher la carte mise à jour
    st_folium(m, width=700, height=500)

except Exception as e:
    st.error(f"Erreur lors du chargement des données des parkings vélo : {e}")
