"""
Composants de l'interface utilisateur (sidebar, inputs)
"""

from datetime import UTC, datetime, time
from zoneinfo import ZoneInfo

import streamlit as st
from streamlit_searchbox import st_searchbox  # type: ignore

from src.parking_velo.config.filters import ParkingVeloFilters

from .constants import PARIS_CENTER, MAP_STYLES
from .styles import EXPANDER_CSS


PARIS_TZ = ZoneInfo("Europe/Paris")


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

        # Date et heure du trajet
        travel_datetime = _create_travel_datetime_input()

        # Bouton de calcul
        calculation_requested = _create_calculation_button(departure, arrival)

        # Options avancées
        show_parking, map_style, to_parking, get_forecast, parking_filter = _create_advanced_options()

        return (
            departure,
            arrival,
            travel_datetime,
            calculation_requested,
            show_parking,
            map_style,
            to_parking,
            get_forecast,
            parking_filter,
        )


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


def _create_travel_datetime_input():
    """Crée les entrées de date et heure du trajet utilisateur."""
    st.markdown(EXPANDER_CSS, unsafe_allow_html=True)

    stored_datetime = st.session_state.get("travel_datetime", datetime.now(PARIS_TZ))
    stored_datetime = stored_datetime.astimezone(PARIS_TZ)

    with st.expander("🕑 heure de depart", expanded=False):
        default_time = time(hour=stored_datetime.hour, minute=stored_datetime.minute)

        selected_date = st.date_input(
            "Date",
            value=stored_datetime.date(),
            key="travel_date",
        )
        selected_time = st.time_input(
            "Heure",
            value=default_time,
            key="travel_time",
        )

        combined_datetime = datetime.combine(selected_date, selected_time, tzinfo=PARIS_TZ)
        st.session_state.travel_datetime = combined_datetime
        return combined_datetime.astimezone(UTC)

    st.session_state.travel_datetime = stored_datetime
    return stored_datetime.astimezone(UTC)


def _create_advanced_options():
    """Crée les options avancées."""
    st.markdown("---")  # Séparateur

    # CSS pour le bouton options sans bords
    st.markdown(EXPANDER_CSS, unsafe_allow_html=True)

    with st.expander("⚙️ Options", expanded=False):
        show_parking = st.checkbox("Afficher les parkings vélo sur la carte", value=True)
        to_parking = st.checkbox(
            "Passer par un parking vélo proche de l'arrivée (segment marche)",
            value=True,
            help=("Si décoché: le vélo va directement à la destination, "
                  "sans segment marche ajouté."),
        )
        map_style = st.selectbox(
            "Style carte",
            options=MAP_STYLES,
            index=0
        )
        available_filters = list(ParkingVeloFilters)
        default_filter = st.session_state.get("parking_filter", ParkingVeloFilters.default)
        try:
            default_index = available_filters.index(default_filter)
        except ValueError:
            default_index = available_filters.index(ParkingVeloFilters.default)

        def _format_filter(filter_value: ParkingVeloFilters) -> str:
            labels = {
                ParkingVeloFilters.privee_abris: "Privé (abri)",
                ParkingVeloFilters.clientele_abris: "Clientèle (abri)",
                ParkingVeloFilters.casier: "Casier sécurisé",
                ParkingVeloFilters.surveille: "Surveillé",
                ParkingVeloFilters.default: "Tous parkings",
            }
            return labels.get(filter_value, str(filter_value))

        parking_filter = st.selectbox(
            "Type de parking vélo",
            options=available_filters,
            index=default_index,
            format_func=_format_filter,
            help="Sélectionne le type d'abri vélo privilégié pour la recherche.",
        )
        st.session_state.parking_filter = parking_filter

        get_forecast = st.checkbox(
            "Afficher les prévisions météo du trajet",
            value=True,
            help="Récupère et affiche la température et les conditions prévues pour l'horaire choisi.",
        )

    return show_parking, map_style, to_parking, get_forecast, parking_filter
