"""
Gestion des itinéraires et des tracés sur la carte
"""

import folium
import polyline  # type: ignore
import streamlit as st

from .constants import ROUTE_COLORS
from .styles import ROUTE_BUTTONS_CSS


def _ensure_dict(data):
    """Retourne le premier dictionnaire trouvé dans une éventuelle liste."""
    if isinstance(data, dict):
        return data
    if isinstance(data, list):
        return next((item for item in data if isinstance(item, dict)), None)
    return None


def _ensure_dict_list(data):
    """Normalise une structure en liste de dictionnaires."""
    if isinstance(data, dict):
        return [data]
    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)]
    return []


def _extract_geojson_coordinates(geojson):
    """Transforme un GeoJSON en liste de points [latitude, longitude]."""
    if not isinstance(geojson, dict):
        return []

    coords = geojson.get('coordinates')
    if not coords:
        return []

    gtype = (geojson.get('type') or '').lower()

    if gtype == 'linestring':
        return [
            [point[1], point[0]]
            for point in coords
            if isinstance(point, (list, tuple)) and len(point) >= 2
        ]

    if gtype == 'multilinestring':
        flattened = []
        for line in coords:
            if not isinstance(line, (list, tuple)):
                continue
            for point in line:
                if isinstance(point, (list, tuple)) and len(point) >= 2:
                    flattened.append([point[1], point[0]])
        return flattened

    return []


def _get_transport_sections(itinerary_data):
    if not itinerary_data:
        return []
    return _ensure_dict_list(itinerary_data.get('itinerary_transport'))


def _transport_duration_minutes_from_sections(sections):
    total_seconds = 0
    for section in sections:
        duration = section.get('duration') if isinstance(section, dict) else None
        if isinstance(duration, (int, float)):
            total_seconds += duration
    if not total_seconds:
        return 0
    return int(round(total_seconds / 60))


def _transport_duration_minutes(itinerary_data):
    return _transport_duration_minutes_from_sections(_get_transport_sections(itinerary_data))


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

    walk_data = _ensure_dict(itinerary_data.get('itinerary_marche'))
    if walk_data:
        walk_duration = walk_data.get('duration', 0) // 60
        walk_distance = walk_data.get('distances', {}).get('walking', 0)
        total_duration += walk_duration
        total_distance += walk_distance

    transport_duration = _transport_duration_minutes(itinerary_data)
    if transport_duration:
        total_duration += transport_duration

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
    walk_data = _ensure_dict(itinerary_data.get('itinerary_marche'))
    if walk_data:
        walk_duration_min = walk_data.get('duration', 0) // 60

    transport_duration_min = _transport_duration_minutes(itinerary_data)

    segment_parts = [f"🚴 {bike_duration}"]
    if transport_duration_min > 0:
        segment_parts.append(f"🚆 {transport_duration_min}")
    if walk_duration_min > 0:
        segment_parts.append(f"🚶 {walk_duration_min}")

    segments_text = " +".join(segment_parts)
    return (f"{title}\n{total_duration} min ({segments_text}) • "
            f"{total_distance/1000:.1f} km")


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
    walk_data = _ensure_dict(itinerary_data.get('itinerary_marche'))
    if walk_data:
        walk_duration_min = walk_data.get('duration', 0) // 60
        total_duration_min += walk_duration_min

    transport_duration_min = _transport_duration_minutes(itinerary_data)
    if transport_duration_min:
        total_duration_min += transport_duration_min

    # Afficher le détail
    segments = [f"{bike_duration_min}min vélo"]
    if transport_duration_min:
        segments.append(f"{transport_duration_min}min transport")
    if walk_duration_min:
        segments.append(f"{walk_duration_min}min marche")

    if segments:
        breakdown = " + ".join(segments)
        st.info(
            f"🎯 **{route_title}** sélectionné : {total_duration_min} minutes total "
            f"({breakdown}), {distance_m/1000:.1f} km"
        )
    else:
        st.info(
            f"🎯 **{route_title}** sélectionné : {bike_duration_min} minutes, "
            f"{distance_m/1000:.1f} km"
        )


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
    walk_data = _ensure_dict(itinerary_data.get('itinerary_marche'))
    if not walk_data:
        return False

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

    walk_data = _ensure_dict(itinerary_data.get('itinerary_marche'))
    if not walk_data:
        return

    duration_min = walk_data.get('duration', 0) // 60
    distance_m = walk_data.get('distances', {}).get('walking', 0)

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


def display_transport_itinerary(transport_data):
    """Affiche un résumé d'un itinéraire de transports en commun."""
    sections = _ensure_dict_list(transport_data)
    if not sections:
        return

    st.markdown("---")
    with st.expander("🚆 Option transports en commun", expanded=False):
        duration_minutes = _transport_duration_minutes_from_sections(sections)
        co2_values = []
        co2_unit = ''
        for section in sections:
            emission = section.get('co2_emission') or {}
            value = emission.get('value')
            if isinstance(value, (int, float)):
                co2_values.append(value)
                if not co2_unit:
                    co2_unit = emission.get('unit', '')
        co2_total = sum(co2_values) if co2_values else None

        transfers = max(len(sections) - 1, 0)

        col_total, col_transfers, col_co2 = st.columns(3)
        col_total.metric("Durée totale", f"{duration_minutes} min")
        col_transfers.metric("Correspondances", str(transfers))
        if isinstance(co2_total, (int, float)):
            col_co2.metric("CO₂", f"{co2_total:.0f} {co2_unit}")
        else:
            col_co2.metric("CO₂", "N/A")

        origin = _section_point_name(sections[0].get('from'))
        destination = _section_point_name(sections[-1].get('to'))
        if origin and destination:
            st.caption(f"Trajet : {origin} → {destination}")

        st.markdown("**Détails des étapes**")
        for section in sections:
            description = _describe_transport_section(section)
            if description:
                st.markdown(f"- {description}")


def add_transport_route_to_map(map_obj, itinerary_data):
    """Trace les segments de transport en commun sur la carte."""
    sections = _get_transport_sections(itinerary_data)
    if not sections:
        return

    for section in sections:
        coords = _extract_geojson_coordinates(section.get('geojson'))
        if not coords:
            continue

        color, dash, weight = _transport_section_style(section)
        popup = _describe_transport_section(section, include_duration=True)

        try:
            folium.PolyLine(
                locations=coords,
                color=color,
                weight=weight,
                opacity=0.85,
                dash_array=dash,
                popup=popup or None,
            ).add_to(map_obj)
        except Exception as exc:
            st.warning(f"Erreur lors de l'affichage du transport : {exc}")


def _transport_section_style(section):
    """Détermine le style du tracé en fonction du mode de transport."""
    display = section.get('display_informations') or {}
    candidates = (
        display.get('physical_mode'),
        display.get('commercial_mode'),
        display.get('code'),
        section.get('mode') or section.get('type'),
    )

    for candidate in candidates:
        if not candidate:
            continue
        descriptor = str(candidate).lower()
        if 'metro' in descriptor:
            return '#ff6f61', None, 5
        if ('rer' in descriptor or 'rail' in descriptor or
                'train' in descriptor):
            return '#1f77b4', None, 5
        if 'tram' in descriptor:
            return '#2ca02c', None, 5
        if 'bus' in descriptor:
            return '#9467bd', None, 4
        if 'walk' in descriptor or 'marche' in descriptor:
            return '#8a2be2', '6,4', 3
        if 'bike' in descriptor or 'velo' in descriptor:
            return '#ffb347', '4,4', 3

    return '#444444', None, 4


def _section_point_name(point):
    if not isinstance(point, dict):
        return None

    stop_point = point.get('stop_point')
    if isinstance(stop_point, dict):
        return stop_point.get('label') or stop_point.get('name')

    return point.get('name') or point.get('label')


def _describe_transport_section(section, include_duration: bool = False):
    display = section.get('display_informations') or {}
    commercial_mode = display.get('commercial_mode')
    physical_mode = display.get('physical_mode')
    code = display.get('code')
    headsign = display.get('headsign')
    section_mode = section.get('mode') or section.get('type')

    mode_label = (commercial_mode or physical_mode or section_mode or 'Trajet')
    mode_label = str(mode_label).replace('_', ' ').title()
    if code:
        mode_label = f"{mode_label} {code}"
    if headsign:
        mode_label = f"{mode_label} → {headsign}"

    origin = _section_point_name(section.get('from'))
    destination = _section_point_name(section.get('to'))

    detail = None
    if origin and destination:
        detail = f"{origin} → {destination}"
    elif origin or destination:
        detail = origin or destination

    duration_text = None
    if include_duration:
        duration = section.get('duration')
        if isinstance(duration, (int, float)) and duration > 0:
            duration_text = f"{int(round(duration / 60))} min"

    parts = [mode_label]
    if detail:
        parts.append(detail)
    if duration_text:
        parts.append(duration_text)

    return " | ".join(parts)
