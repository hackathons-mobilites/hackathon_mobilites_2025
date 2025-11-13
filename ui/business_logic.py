"""
Logique métier pour l'application Vel'Octo
"""

import streamlit as st

from .constants import DEBUG_ADDRESSES
from src.itineraire.domain.apps.itineraire_velo import itineraire_parking_velo


def init_session_state():
    """Initialise les variables de session."""
    if "departure_selected" not in st.session_state:
        st.session_state.departure_selected = DEBUG_ADDRESSES["departure"]
    if "arrival_selected" not in st.session_state:
        st.session_state.arrival_selected = DEBUG_ADDRESSES["arrival"]

    # DEBUG: Forcer les valeurs pour les tests
    st.session_state.departure_selected = DEBUG_ADDRESSES["departure"]
    st.session_state.arrival_selected = DEBUG_ADDRESSES["arrival"]


def calculate_itinerary(departure, arrival):
    """Calcule l'itinéraire entre deux points."""
    with st.spinner("Calcul en cours..."):
        try:
            result = itineraire_parking_velo(departure, arrival)

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
