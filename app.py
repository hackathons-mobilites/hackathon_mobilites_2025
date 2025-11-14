"""
Application principale CycloFlow - Planification d'itinéraires vélo
"""

import streamlit as st
import googlemaps  # type: ignore
from streamlit_folium import st_folium  # type: ignore

from config.var_env import GOOGLE_MAP_API_KEY
from ui import (
    init_session_state,
    calculate_itinerary,
    has_itinerary_result,
    get_itinerary_result,
    create_base_map,
    add_bike_routes_to_map,
    add_departure_arrival_markers,
    add_walking_route_to_map,
    create_sidebar,
    display_weather_forecast,
)

# Configuration de la page
st.set_page_config(page_title="CycloFlow", page_icon="🚴", layout="centered")
st.markdown("<h1 style='text-align: center;'>🚴 CycloFlow</h1>", unsafe_allow_html=True)


def main():
    """Fonction principale de l'application."""
    # Initialisation
    init_session_state()
    gmaps = googlemaps.Client(key=GOOGLE_MAP_API_KEY)

    # Interface utilisateur - Sidebar
    (
        departure,
        arrival,
        travel_datetime,
        calculation_requested,
        show_parking,
        map_style,
        to_parking,
        get_forecast,
    ) = create_sidebar(gmaps)

    # Calcul d'itinéraire si demandé
    if calculation_requested:
        calculate_itinerary(
            departure,
            arrival,
            to_parking,
            travel_datetime,
            get_forecast,
        )

    # Créer la carte avec les options sélectionnées
    m = create_base_map(show_parking, map_style)

    # Affichage des résultats d'itinéraire
    if has_itinerary_result():
        try:
            itinerary_data = get_itinerary_result()
            if itinerary_data.get("meteo_forecast"):
                display_weather_forecast(
                    itinerary_data["meteo_forecast"],
                    st.session_state.get("travel_datetime"),
                )
            add_departure_arrival_markers(m, itinerary_data)
            add_bike_routes_to_map(m, itinerary_data)
            add_walking_route_to_map(m, itinerary_data)
        except Exception as e:
            st.error(f"❌ Erreur affichage: {e}")

    # Carte finale
    st_folium(m, width=700, height=500)


if __name__ == "__main__":
    main()
