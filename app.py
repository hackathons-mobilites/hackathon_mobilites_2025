import streamlit as st
import folium
from streamlit_folium import st_folium
from src.parking_velo.domain.apps.get_parking_velo import get_parking_velo
from src.parking_velo.config.filters import ParkingVeloFilters
from folium.plugins import MarkerCluster
import json
import polyline
# Importer la clé API Google Maps
from config.var_env import GOOGLE_MAP_API_KEY
import googlemaps

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

# Initialiser le client Google Maps
gmaps = googlemaps.Client(key=GOOGLE_MAP_API_KEY)


# Fonction pour obtenir des suggestions d'adresses
def get_address_suggestions(query):
    if not query:
        return []
    try:
        # Bias géographique (Paris) pour de meilleurs résultats locaux
        results = gmaps.places_autocomplete(
            query,
            location=(48.8566, 2.3522),  # Paris centre
            radius=50000  # 50 km
        )
        suggestions = [result['description'] for result in results]
        if debug_mode:
            st.sidebar.write(f"Suggestions brutes: {suggestions}")
        return suggestions
    except Exception:
        st.sidebar.warning("Impossible de récupérer des suggestions (quota, clé ou réseau).")
        return []


# Ajouter les champs avec autocomplétion
st.sidebar.header("Itinéraire")
debug_mode = st.sidebar.checkbox("Mode debug", value=False)

# Import composant d'autocomplétion (fallback si non installé)
try:
    from streamlit_searchbox import st_searchbox
    searchbox_available = True
except Exception:
    searchbox_available = False
    st.sidebar.warning("Module streamlit-searchbox non installé. Utilisation mode dégradé.")  # type: ignore

# États
for key in ["departure_selected", "arrival_selected"]:
    if key not in st.session_state:
        st.session_state[key] = None


def autocomplete_places_depart(query: str) -> list:
    if len(query) < 3:
        return []
    return get_address_suggestions(query)


def autocomplete_places_arrival(query: str) -> list:
    if len(query) < 3:
        return []
    return get_address_suggestions(query)


with st.sidebar.container():
    st.subheader("Départ")
    if searchbox_available:
        dep_choice = st_searchbox(
            autocomplete_places_depart,
            key="departure_searchbox",
            placeholder="Tapez l'adresse de départ"
        )
    else:
        dep_query = st.text_input("Adresse de départ (fallback)", key="dep_query_fb")
        dep_suggestions = autocomplete_places_depart(dep_query)
        dep_choice = st.selectbox("Suggestions", dep_suggestions if dep_suggestions else [""], key="dep_select_fb")
    if dep_choice:
        st.session_state.departure_selected = dep_choice
        try:
            geocode_dep = gmaps.geocode(dep_choice)
            if geocode_dep:
                loc_dep = geocode_dep[0]["geometry"]["location"]
                folium.Marker(
                    location=(loc_dep["lat"], loc_dep["lng"]),
                    popup=f"Départ: {dep_choice}",
                    icon=folium.Icon(color="green", icon="play")
                ).add_to(m)
                if debug_mode:
                    st.sidebar.write(f"Départ géocodé: {loc_dep}")
        except Exception:
            st.sidebar.warning("Échec géocodage départ.")

with st.sidebar.container():
    st.subheader("Arrivée")
    if searchbox_available:
        arr_choice = st_searchbox(
            autocomplete_places_arrival,
            key="arrival_searchbox",
            placeholder="Tapez l'adresse d'arrivée"
        )
    else:
        arr_query = st.text_input("Adresse d'arrivée (fallback)", key="arr_query_fb")
        arr_suggestions = autocomplete_places_arrival(arr_query)
        arr_choice = st.selectbox("Suggestions", arr_suggestions if arr_suggestions else [""], key="arr_select_fb")
    if arr_choice:
        st.session_state.arrival_selected = arr_choice
        try:
            geocode_arr = gmaps.geocode(arr_choice)
            if geocode_arr:
                loc_arr = geocode_arr[0]["geometry"]["location"]
                folium.Marker(
                    location=(loc_arr["lat"], loc_arr["lng"]),
                    popup=f"Arrivée: {arr_choice}",
                    icon=folium.Icon(color="red", icon="flag")
                ).add_to(m)
                if debug_mode:
                    st.sidebar.write(f"Arrivée géocodée: {loc_arr}")
        except Exception:
            st.sidebar.warning("Échec géocodage arrivée.")
