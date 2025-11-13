"""
Gestion des cartes Folium pour Vel'Octo
"""

import folium
from folium.plugins import MarkerCluster
import streamlit as st

from .constants import (
    DEFAULT_USER_LOCATION,
    ESRI_URLS,
    ATTR_MAP
)
from .styles import MAP_ATTRIBUTION_CSS
from src.parking_velo.domain.apps.get_parking_velo import get_parking_velo
from src.parking_velo.config.filters import ParkingVeloFilters


@st.cache_data
def load_parking_data():
    """Charge les données des parkings vélo."""
    return get_parking_velo(filter=ParkingVeloFilters.privee_abris)


def create_base_map(show_parking=True, map_style='OpenStreetMap'):
    """Crée la carte de base avec marqueur utilisateur et parkings."""
    m = _create_map_with_style(map_style)

    # Injecter le CSS pour nettoyer les attributions
    st.markdown(MAP_ATTRIBUTION_CSS, unsafe_allow_html=True)

    # Ajouter les marqueurs par défaut
    m = add_default_markers(m, show_parking)

    return m


def _create_map_with_style(map_style):
    """Crée une carte avec le style spécifié."""
    if map_style.startswith('Esri'):
        return _create_esri_map(map_style)
    elif map_style == 'CartoDB Voyager':
        return _create_cartodb_voyager_map()
    else:
        return _create_standard_map(map_style)


def _create_esri_map(map_style):
    """Crée une carte Esri."""
    m = folium.Map(
        location=DEFAULT_USER_LOCATION,
        zoom_start=12,
        prefer_canvas=True
    )

    folium.TileLayer(
        tiles=ESRI_URLS.get(map_style, ESRI_URLS['Esri WorldImagery']),
        attr='Esri',
        name=map_style,
        overlay=False,
        control=True
    ).add_to(m)

    return m


def _create_cartodb_voyager_map():
    """Crée une carte CartoDB Voyager."""
    m = folium.Map(
        location=DEFAULT_USER_LOCATION,
        zoom_start=12,
        prefer_canvas=True
    )

    folium.TileLayer(
        tiles='https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png',
        attr='CARTO',
        name='CartoDB Voyager',
        overlay=False,
        control=True
    ).add_to(m)

    return m


def _create_standard_map(map_style):
    """Crée une carte standard (OpenStreetMap, CartoDB)."""
    return folium.Map(
        location=DEFAULT_USER_LOCATION,
        zoom_start=12,
        tiles=map_style,
        attr=ATTR_MAP.get(map_style, 'Map tiles'),
        prefer_canvas=True
    )


def add_default_markers(m, show_parking=True):
    """Ajoute les marqueurs par défaut (utilisateur et parkings)."""
    # Marqueur utilisateur
    folium.Marker(
        location=DEFAULT_USER_LOCATION,
        popup="Vous êtes ici",
        icon=folium.DivIcon(
            html='<i class="fa fa-user" style="color: red; font-size: 16px;"></i>',
            icon_size=(20, 20),
            icon_anchor=(10, 10)
        )
    ).add_to(m)

    # Ajouter parkings vélo si demandé
    if show_parking:
        _add_parking_markers(m)

    return m


def _add_parking_markers(m):
    """Ajoute les marqueurs de parkings vélo."""
    # Cluster pour parkings avec configuration pour bulles plus petites
    marker_cluster = MarkerCluster(
        max_cluster_radius=30,
        icon_create_function="""
        function(cluster) {
            var count = cluster.getChildCount();
            var size = count < 10 ? 'small' : count < 100 ? 'medium' : 'large';
            var sizeMap = {'small': 20, 'medium': 30, 'large': 40};
            return L.divIcon({
                html: '<div><span>' + count + '</span></div>',
                className: 'marker-cluster marker-cluster-' + size,
                iconSize: new L.Point(sizeMap[size], sizeMap[size])
            });
        }"""
    ).add_to(m)

    try:
        parking_data = load_parking_data()
        for _, row in parking_data.iterrows():
            folium.Marker(
                location=[row.geometry.y, row.geometry.x],
                popup=f"Parking ID: {row.get('osm_id', 'N/A')}<br>Capacité: {row.get('capacite', 'N/A')}",
                icon=folium.DivIcon(
                    html='<i class="fa fa-bicycle" style="color: green; font-size: 12px;"></i>',
                    icon_size=(16, 16),
                    icon_anchor=(8, 8)
                )
            ).add_to(marker_cluster)

        st.write(f"✅ {len(parking_data)} parkings vélo chargés")
    except Exception as e:
        st.error(f"❌ Erreur chargement parkings: {e}")
