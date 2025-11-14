"""
Gestion des itinéraires et des tracés sur la carte
"""

import folium
import polyline  # type: ignore
import streamlit as st

from .constants import ROUTE_COLORS
from .styles import ROUTE_BUTTONS_CSS


def add_bike_routes_to_map(map_obj, itinerary_data):
    """Ajoute les itinéraires vélo à la carte."""
    if 'itinerary_velo' not in itinerary_data:
        return

    st.write("**🚴‍♂️ Itinéraires vélo disponibles**")

    # Initialiser l'itinéraire sélectionné
    if 'selected_route' not in st.session_state:
        st.session_state.selected_route = None

    # Préparer les données des boutons
    route_buttons = _prepare_route_buttons_data(itinerary_data)

    # Afficher les boutons d'itinéraires
    if route_buttons:
        _display_route_buttons(route_buttons, itinerary_data)

    # Ajouter tous les tracés à la carte
    _add_route_polylines(map_obj, itinerary_data)

    # Afficher les détails de l'itinéraire sélectionné
    _display_selected_route_details(itinerary_data)


def _prepare_route_buttons_data(itinerary_data):
    """Prépare les données pour les boutons d'itinéraires."""
    route_buttons = []

    for i, route in enumerate(itinerary_data['itinerary_velo']):
        route_title = route.get('title', 'Route inconnue')
        duration_min = route.get('duration', 0) // 60
        distance_m = route.get('distances', {}).get('total', 0)

        # Calculer les totaux avec la marche
        total_duration_min, total_distance_m = _calculate_totals(
            duration_min, distance_m, itinerary_data
        )

        route_buttons.append((
            route, i, route_title, duration_min, distance_m,
            total_duration_min, total_distance_m
        ))

    return route_buttons


def _calculate_totals(bike_duration, bike_distance, itinerary_data):
    """Calcule les durées et distances totales (vélo + marche)."""
    total_duration = bike_duration
    total_distance = bike_distance

    if 'itinerary_marche' in itinerary_data and itinerary_data['itinerary_marche']:
        walk_data = itinerary_data['itinerary_marche']
        walk_duration = walk_data.get('duration', 0) // 60
        walk_distance = walk_data.get('distances', {}).get('walking', 0)
        total_duration += walk_duration
        total_distance += walk_distance

    return total_duration, total_distance


def _display_route_buttons(route_buttons, itinerary_data):
    """Affiche les boutons d'itinéraires."""
    # Ajouter le CSS pour les boutons
    st.markdown(ROUTE_BUTTONS_CSS, unsafe_allow_html=True)

    cols = st.columns(len(route_buttons))
    for col, route_info in zip(cols, route_buttons):
        (route_data, route_index, title, duration, distance,
         total_duration, total_distance) = route_info

        with col:
            button_text = _create_button_text(
                title, duration, total_duration, total_distance, itinerary_data
            )

            is_selected = st.session_state.selected_route == route_index
            button_type = "primary" if is_selected else "secondary"

            if st.button(
                button_text,
                key=f"route_btn_{route_index}",
                type=button_type,
                use_container_width=True
            ):
                st.session_state.selected_route = route_index
                st.rerun()


def _create_button_text(title, bike_duration, total_duration, total_distance, itinerary_data):
    """Crée le texte du bouton d'itinéraire."""
    walk_duration_min = 0
    if 'itinerary_marche' in itinerary_data and itinerary_data['itinerary_marche']:
        walk_duration_min = itinerary_data['itinerary_marche'].get('duration', 0) // 60

    if walk_duration_min > 0:
        return (f"{title}\n{total_duration} min (🚴 {bike_duration} +🚶{walk_duration_min}) • "
                f"{total_distance/1000:.1f} km")
    else:
        return f"{title}\n🚴{total_duration} min • {total_distance/1000:.1f} km"


def _add_route_polylines(map_obj, itinerary_data):
    """Ajoute tous les tracés d'itinéraires à la carte."""
    for i, route in enumerate(itinerary_data['itinerary_velo']):
        route_title = route.get('title', 'Route inconnue')
        duration_min = route.get('duration', 0) // 60
        distance_m = route.get('distances', {}).get('total', 0)

        for section in route.get('sections', []):
            encoded_geometry = section.get('geometry')
            if encoded_geometry:
                try:
                    decoded_path = polyline.decode(encoded_geometry, precision=6)
                    color = ROUTE_COLORS.get(route_title, '#666666')

                    # Style selon si l'itinéraire est sélectionné
                    opacity = 1.0 if st.session_state.selected_route == i else 0.4
                    weight = 5 if st.session_state.selected_route == i else 3

                    folium.PolyLine(
                        locations=decoded_path,
                        color=color,
                        weight=weight,
                        opacity=opacity,
                        popup=f"{route_title} - {duration_min}min - {distance_m}m"
                    ).add_to(map_obj)
                except Exception as e:
                    st.warning(f"Erreur géométrie {route_title}: {e}")


def _display_selected_route_details(itinerary_data):
    """Affiche les détails de l'itinéraire sélectionné."""
    if (st.session_state.selected_route is None or
            st.session_state.selected_route >= len(itinerary_data['itinerary_velo'])):
        return

    selected_route = itinerary_data['itinerary_velo'][st.session_state.selected_route]
    route_title = selected_route.get('title', 'Route inconnue')
    bike_duration_min = selected_route.get('duration', 0) // 60
    distance_m = selected_route.get('distances', {}).get('total', 0)

    # Calculer le temps total
    total_duration_min = bike_duration_min
    walk_duration_min = 0
    if 'itinerary_marche' in itinerary_data and itinerary_data['itinerary_marche']:
        walk_duration_min = itinerary_data['itinerary_marche'].get('duration', 0) // 60
        total_duration_min += walk_duration_min

    # Afficher le détail
    if walk_duration_min > 0:
        st.info(f"🎯 **{route_title}** sélectionné : {total_duration_min} minutes total "
                f"({bike_duration_min}min vélo + {walk_duration_min}min marche), "
                f"{distance_m/1000:.1f} km")
    else:
        st.info(f"🎯 **{route_title}** sélectionné : {bike_duration_min} minutes, "
                f"{distance_m/1000:.1f} km")


def add_departure_arrival_markers(map_obj, itinerary_data):
    """Ajoute les marqueurs de départ et d'arrivée sur la carte."""
    if not _validate_itinerary_data(itinerary_data):
        return

    first_route = itinerary_data['itinerary_velo'][0]
    waypoints = first_route.get('waypoints', [])

    # Point de départ
    if waypoints:
        _add_departure_marker(map_obj, waypoints[0])

    # Point d'arrivée
    _add_arrival_marker(map_obj, itinerary_data, waypoints)


def _validate_itinerary_data(itinerary_data):
    """Valide les données d'itinéraire."""
    return (itinerary_data and
            'itinerary_velo' in itinerary_data and
            itinerary_data['itinerary_velo'])


def _add_departure_marker(map_obj, start_waypoint):
    """Ajoute le marqueur de départ."""
    start_lat = start_waypoint.get('latitude')
    start_lon = start_waypoint.get('longitude')

    if start_lat and start_lon:
        folium.Marker(
            location=[start_lat, start_lon],
            popup="🚀 Point de départ",
            icon=folium.DivIcon(
                html='<i class="fa fa-play" style="color: blue; font-size: 16px;"></i>',
                icon_size=(20, 20),
                icon_anchor=(10, 10)
            )
        ).add_to(map_obj)


def _add_arrival_marker(map_obj, itinerary_data, waypoints):
    """Ajoute le marqueur d'arrivée."""
    # Chercher dans l'itinéraire à pied d'abord
    if _add_walking_destination_marker(map_obj, itinerary_data):
        return

    # Fallback sur le dernier waypoint vélo
    if len(waypoints) >= 2:
        _add_bike_destination_marker(map_obj, waypoints[-1])


def _add_walking_destination_marker(map_obj, itinerary_data):
    """Ajoute le marqueur de destination finale depuis l'itinéraire à pied."""
    if not (itinerary_data.get('itinerary_marche')):
        return False

    walk_data = itinerary_data['itinerary_marche']
    walk_sections = walk_data.get('sections', [])

    for section in walk_sections:
        if (_has_valid_geojson(section)):
            coords = section['geojson']['coordinates']
            if coords:
                final_coord = coords[-1]
                if len(final_coord) >= 2:
                    folium.Marker(
                        location=[final_coord[1], final_coord[0]],
                        popup="🏁 Destination finale",
                        icon=folium.DivIcon(
                            html='<i class="fa fa-stop" style="color: orange; font-size: 16px;"></i>',
                            icon_size=(20, 20),
                            icon_anchor=(10, 10)
                        )
                    ).add_to(map_obj)
                    return True

    return False


def _has_valid_geojson(section):
    """Vérifie si une section a une géométrie GeoJSON valide."""
    return ('geojson' in section and
            section['geojson'] and
            section['geojson'].get('type') == 'LineString' and
            'coordinates' in section['geojson'])


def _add_bike_destination_marker(map_obj, end_waypoint):
    """Ajoute le marqueur de destination vélo."""
    end_lat = end_waypoint.get('latitude')
    end_lon = end_waypoint.get('longitude')

    if end_lat and end_lon:
        folium.Marker(
            location=[end_lat, end_lon],
            popup="🏁 Parking vélo (arrivée)",
            icon=folium.DivIcon(
                html='<i class="fa fa-stop" style="color: orange; font-size: 16px;"></i>',
                icon_size=(20, 20),
                icon_anchor=(10, 10)
            )
        ).add_to(map_obj)


def add_walking_route_to_map(map_obj, itinerary_data):
    """Ajoute l'itinéraire à pied à la carte."""
    if not itinerary_data or 'itinerary_marche' not in itinerary_data:
        return

    walk_data = itinerary_data['itinerary_marche']
    if not walk_data:
        return

    st.write("**🚶‍♂️ Itinéraire à pied (parking → destination)**")

    duration_min = walk_data.get('duration', 0) // 60
    distance_m = walk_data.get('distances', {}).get('walking', 0)

    st.write(f"**Trajet à pied** : {duration_min} min • {distance_m} m")

    # Ajouter le tracé à pied
    for section in walk_data.get('sections', []):
        if _has_valid_geojson(section):
            coords = section['geojson']['coordinates']
            if coords:
                try:
                    folium_coords = [[coord[1], coord[0]]
                                     for coord in coords if len(coord) >= 2]
                    if folium_coords:
                        folium.PolyLine(
                            locations=folium_coords,
                            color='purple',
                            weight=4,
                            opacity=0.8,
                            dash_array='8, 4',
                            popup=f"🚶‍♂️ À pied - {duration_min}min - {distance_m}m"
                        ).add_to(map_obj)
                except (IndexError, TypeError) as e:
                    st.warning(f"Erreur lors de l'affichage de l'itinéraire à pied: {e}")
