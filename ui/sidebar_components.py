"""
Composants de l'interface utilisateur (sidebar, inputs)
"""

import streamlit as st
from streamlit_searchbox import st_searchbox  # type: ignore

from .constants import PARIS_CENTER, MAP_STYLES
from .styles import EXPANDER_CSS


def get_address_suggestions(query, gmaps):
    """Obtient des suggestions d'adresses via Google Maps."""
    if not query or len(query) < 3:
        return []
    try:
        results = gmaps.places_autocomplete(query, location=PARIS_CENTER, radius=50000)
        return [result['description'] for result in results]
    except Exception:
        return []


def create_address_input(label, key_prefix, default_value, gmaps):
    """Crée un champ de saisie d'adresse avec autocomplétion."""
    st.subheader(label)

    # Tentative d'utilisation de streamlit-searchbox
    try:
        choice = st_searchbox(
            lambda query: get_address_suggestions(query, gmaps),
            key=f"{key_prefix}_searchbox",
            placeholder=f"Tapez l'adresse de {label.lower()}",
            default=default_value
        )
    except ImportError:
        # Fallback en mode dégradé
        st.warning("Module streamlit-searchbox non disponible")
        query = st.text_input(f"Adresse de {label.lower()}",
                              key=f"{key_prefix}_fb",
                              value=default_value)
        suggestions = get_address_suggestions(query, gmaps)
        choice = st.selectbox("Suggestions", suggestions if suggestions else [query],
                              key=f"{key_prefix}_select") if suggestions else query

    return choice


def create_sidebar(gmaps):
    """Crée la sidebar avec tous les contrôles."""
    with st.sidebar:
        st.header("🗺️ Planification d'itinéraire")

        # Champs d'adresses
        departure, arrival = _create_address_inputs(gmaps)

        # Bouton de calcul
        calculation_requested = _create_calculation_button(departure, arrival)

        # Options avancées
        show_parking, map_style = _create_advanced_options()

        return departure, arrival, calculation_requested, show_parking, map_style


def _create_address_inputs(gmaps):
    """Crée les champs de saisie d'adresses."""
    departure = create_address_input(
        "Départ",
        "departure",
        st.session_state.departure_selected,
        gmaps
    )
    arrival = create_address_input(
        "Arrivée",
        "arrival",
        st.session_state.arrival_selected,
        gmaps
    )

    # Mise à jour session state
    if departure:
        st.session_state.departure_selected = departure
    if arrival:
        st.session_state.arrival_selected = arrival

    return departure, arrival


def _create_calculation_button(departure, arrival):
    """Crée le bouton de calcul d'itinéraire."""
    if st.button("🚴 Calculer l'itinéraire", type="primary", use_container_width=True):
        if departure and arrival:
            return True
        else:
            st.warning("⚠️ Sélectionnez départ et arrivée")

    return False


def _create_advanced_options():
    """Crée les options avancées."""
    st.markdown("---")  # Séparateur

    # CSS pour le bouton options sans bords
    st.markdown(EXPANDER_CSS, unsafe_allow_html=True)

    with st.expander("⚙️ Options", expanded=False):
        show_parking = st.checkbox("Parkings vélo", value=True)
        map_style = st.selectbox(
            "Style carte",
            options=MAP_STYLES,
            index=0
        )

    return show_parking, map_style
