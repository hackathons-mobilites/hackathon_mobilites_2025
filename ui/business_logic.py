"""
Logique métier pour l'application CycloFlow
"""

import logging
from collections import OrderedDict
from copy import deepcopy
from datetime import datetime
from typing import Any, Dict, Iterable, List, Optional

import streamlit as st

from .constants import DEBUG_ADDRESSES
from src.parking_velo.config.filters import ParkingVeloFilters
from src.itineraire.domain.apps.itineraire_velo import itineraire_parking_velo


def init_session_state():
    """Initialise les variables de session."""
    if "departure_selected" not in st.session_state:
        st.session_state.departure_selected = DEBUG_ADDRESSES["departure"]
    if "arrival_selected" not in st.session_state:
        st.session_state.arrival_selected = DEBUG_ADDRESSES["arrival"]
    if "parking_filter" not in st.session_state:
        st.session_state.parking_filter = ParkingVeloFilters.default

    # DEBUG: Forcer les valeurs pour les tests
    st.session_state.departure_selected = DEBUG_ADDRESSES["departure"]
    st.session_state.arrival_selected = DEBUG_ADDRESSES["arrival"]


def calculate_itinerary(
    departure,
    arrival,
    to_parking: bool = True,
    use_train: bool = True,
    travel_datetime: Optional[datetime] = None,
    get_forecast: bool = False,
    parking_filter: ParkingVeloFilters = ParkingVeloFilters.default,
):
    """Calcule l'itinéraire entre deux points.

    to_parking: si True, l'itinéraire vélo s'arrête au parking puis ajoute un segment de marche.
    Si False, l'itinéraire vélo va directement à l'adresse d'arrivée et aucune clé 'itinerary_marche' n'est renvoyée.
    """
    with st.spinner("Calcul en cours..."):
        try:
            if travel_datetime:
                logging.info("Itinéraire demandé pour %s", travel_datetime.isoformat())
            else:
                logging.info("Itinéraire demandé sans date/heure spécifique")

            st.session_state.get_forecast_requested = get_forecast
            st.session_state.parking_filter = parking_filter
            st.session_state.use_train_enabled = use_train

            result = itineraire_parking_velo(
                departure,
                arrival,
                to_parking,
                travel_datetime=travel_datetime,
                get_forecast=get_forecast,
                parking_filter=parking_filter,
                use_train=use_train,
            )

            result_dict = _first_dict(result)
            if result_dict is None:
                logging.error("Unexpected itinerary response type: %s", type(result))
                st.error("❌ Réponse inattendue du service d'itinéraire")
                return False
            result = result_dict

            normalized_routes = _normalize_bike_itineraries(result.get('itinerary_velo'))
            if normalized_routes:
                result['itinerary_velo'] = normalized_routes

            walk_data = _first_dict(result.get('itinerary_marche'))
            if walk_data:
                result['itinerary_marche'] = walk_data
            elif 'itinerary_marche' in result:
                result.pop('itinerary_marche')

            transport_sections = _to_dict_list(result.get('itinerary_transport'))
            if transport_sections:
                result['itinerary_transport'] = transport_sections
            elif 'itinerary_transport' in result:
                result.pop('itinerary_transport')

            # Vérifier que le résultat contient des données valides
            if not result:
                st.error("❌ Aucun itinéraire trouvé")
                return False
            elif 'itinerary_velo' not in result or not result['itinerary_velo']:
                st.error("❌ Aucun itinéraire vélo trouvé. La distance est peut-être trop importante "
                         "ou aucun parking vélo n'est disponible près de votre destination.")
                return False
            else:
                st.session_state.itinerary_result = result
                st.session_state.selected_route = 0
                st.success("✅ Itinéraire calculé!")
                return True
        except Exception as e:
            st.error(f"❌ Erreur lors du calcul: {str(e)}")
            # Afficher plus de détails en mode debug si nécessaire
            if hasattr(e, '__class__'):
                st.error(f"Type d'erreur: {e.__class__.__name__}")
            return False


def has_itinerary_result():
    """Vérifie si un résultat d'itinéraire est disponible."""
    return (hasattr(st.session_state, 'itinerary_result') and
            st.session_state.itinerary_result)


def get_itinerary_result():
    """Récupère le résultat d'itinéraire."""
    if has_itinerary_result():
        return st.session_state.itinerary_result
    return None


def _first_dict(data: Any) -> Optional[Dict[str, Any]]:
    """Retrouve le premier dictionnaire dans une réponse potentiellement imbriquée."""
    if isinstance(data, dict):
        return data
    if isinstance(data, list):
        for item in data:
            found = _first_dict(item)
            if isinstance(found, dict):
                return found
    return None


def _to_dict_list(data: Any) -> List[Dict[str, Any]]:
    """Normalise une structure en liste de dictionnaires."""
    if isinstance(data, dict):
        return [data]
    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)]
    return []


def _normalize_bike_itineraries(raw_routes: Any) -> List[Dict[str, Any]]:
    """Agrège les itinéraires vélo lorsqu'ils sont fournis par segments.

    Retourne une liste plate d'itinéraires avec les clés attendues par l'UI.
    """
    if not raw_routes or not isinstance(raw_routes, list):
        return []

    # Déjà au format plat attendu
    if all(isinstance(route, dict) for route in raw_routes):
        return raw_routes

    aggregated: "OrderedDict[str, Dict[str, Any]]" = OrderedDict()
    order: List[str] = []

    iterable_segments: Iterable[Any]
    if all(isinstance(route, dict) for route in raw_routes):
        iterable_segments = [raw_routes]
    else:
        iterable_segments = raw_routes

    for segment in iterable_segments:
        if isinstance(segment, dict):
            segment = [segment]
        if not isinstance(segment, list):
            continue

        for option in segment:
            if not isinstance(option, dict):
                continue

            title = option.get('title') or f"Itinéraire {len(order) + 1}"

            if title not in aggregated:
                base = {
                    'title': title,
                    'id': option.get('id'),
                    'duration': 0,
                    'distances': {},
                    'sections': [],
                    'waypoints': [],
                    'details': option.get('details') or {},
                    'segment_details': [],
                    'estimatedDatetimeOfDeparture': None,
                    'estimatedDatetimeOfArrival': None,
                }
                base['_waypoints_seen'] = set()
                base['_departures'] = []
                base['_arrivals'] = []
                aggregated[title] = base
                order.append(title)

            agg = aggregated[title]

            agg['duration'] += option.get('duration', 0) or 0

            for key, value in (option.get('distances') or {}).items():
                if isinstance(value, (int, float)):
                    agg['distances'][key] = agg['distances'].get(key, 0) + value

            if option.get('sections'):
                agg['sections'].extend(deepcopy(option['sections']))

            for waypoint in option.get('waypoints', []):
                if not isinstance(waypoint, dict):
                    continue
                coords = (waypoint.get('longitude'), waypoint.get('latitude'))
                if coords not in agg['_waypoints_seen']:
                    agg['_waypoints_seen'].add(coords)
                    agg['waypoints'].append(deepcopy(waypoint))

            departure = option.get('estimatedDatetimeOfDeparture')
            if departure:
                agg['_departures'].append(departure)
            arrival = option.get('estimatedDatetimeOfArrival')
            if arrival:
                agg['_arrivals'].append(arrival)

            agg['segment_details'].append(deepcopy(option))
            if not agg.get('details') and option.get('details'):
                agg['details'] = option['details']

            if not agg.get('id') and option.get('id'):
                agg['id'] = option.get('id')

    normalized: List[Dict[str, Any]] = []

    for title in order:
        agg = aggregated[title]
        departures = agg.pop('_departures', [])
        arrivals = agg.pop('_arrivals', [])
        agg.pop('_waypoints_seen', None)

        if departures:
            try:
                agg['estimatedDatetimeOfDeparture'] = min(departures)
            except TypeError:
                agg['estimatedDatetimeOfDeparture'] = departures[0]
        if arrivals:
            try:
                agg['estimatedDatetimeOfArrival'] = max(arrivals)
            except TypeError:
                agg['estimatedDatetimeOfArrival'] = arrivals[-1]

        normalized.append(agg)

    return normalized
