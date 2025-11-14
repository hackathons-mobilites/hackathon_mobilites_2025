"""
Application Streamlit pour l'optimisation d'itinéraires multimodaux
Permet de sélectionner des coordonnées sur une carte, choisir date/heure, et rayon
"""

import streamlit as st
import folium
from streamlit_folium import folium_static
import json
from datetime import datetime, timedelta
from route_optimizer import RouteOptimizer
import ast
import requests

# Configuration de la page
st.set_page_config(
    page_title="Optimiseur d'Itinéraires Multimodaux",
    page_icon="🚲🚇",
    layout="wide",
    initial_sidebar_state="expanded"
)

def parse_geojson_string(geojson_str):
    """Parse une string GeoJSON et retourne un dict Python"""
    if not geojson_str or geojson_str == 'None':
        return None
    
    try:
        # Si c'est déjà un dict, on le retourne
        if isinstance(geojson_str, dict):
            return geojson_str
        
        # Si c'est une string, on essaie de la parser
        if isinstance(geojson_str, str):
            # Nettoyer la string et la convertir
            cleaned = geojson_str.strip().strip("'\"")
            return json.loads(cleaned)
    except (json.JSONDecodeError, ValueError) as e:
        st.error(f"Erreur de parsing GeoJSON: {e}")
        return None

def parse_geojson_list(geojson_list_data):
    """Parse une liste de GeoJSON depuis différents formats"""
    if not geojson_list_data or geojson_list_data == 'None':
        return []
    
    try:
        # Si c'est déjà une liste Python (cas direct depuis DataFrame)
        if isinstance(geojson_list_data, list):
            result = []
            for item in geojson_list_data:
                if isinstance(item, str):
                    try:
                        # Chaque élément est une string JSON, on la parse
                        result.append(json.loads(item))
                    except json.JSONDecodeError:
                        st.warning(f"Impossible de parser l'élément GeoJSON: {item[:100]}...")
                        continue
                elif isinstance(item, dict):
                    # Déjà un dict, on l'ajoute directement
                    result.append(item)
            return result
        
        # Si c'est une string qui ressemble à une liste Python
        elif isinstance(geojson_list_data, str):
            # Nettoyer et parser la liste
            cleaned = geojson_list_data.strip().strip("'\"")
            # Utiliser ast.literal_eval pour parser la liste Python
            parsed_list = ast.literal_eval(cleaned)
            
            # Chaque élément de la liste devrait être une string JSON
            result = []
            for item in parsed_list:
                if isinstance(item, str):
                    try:
                        result.append(json.loads(item))
                    except json.JSONDecodeError:
                        continue
                elif isinstance(item, dict):
                    result.append(item)
            
            return result
            
    except Exception as e:
        st.error(f"Erreur de parsing de la liste GeoJSON: {e} - Type: {type(geojson_list_data)}")
        return []

def add_geojson_to_map(folium_map, geojson_data, color, style_type="solid", weight=3):
    """Ajoute des données GeoJSON à une carte Folium avec style personnalisé"""
    if not geojson_data:
        return
    
    # Déterminer le style de ligne
    dash_array = "5,5" if style_type == "dashed" else None
    
    if isinstance(geojson_data, list):
        # Liste de GeoJSON (cas des trajets transport en commun)
        for i, geom in enumerate(geojson_data):
            folium.GeoJson(
                geom,
                style_function=lambda feature, color=color, dash=dash_array, w=weight: {
                    'color': color,
                    'weight': w,
                    'opacity': 0.8,
                    'dashArray': dash
                }
            ).add_to(folium_map)
    else:
        # GeoJSON unique ou FeatureCollection
        folium.GeoJson(
            geojson_data,
            style_function=lambda feature, color=color, dash=dash_array, w=weight: {
                'color': color,
                'weight': w,
                'opacity': 0.8,
                'dashArray': dash
            }
        ).add_to(folium_map)

def create_route_map(route_data, origin_coords, destination_coords):
    """Crée une carte avec tous les GeoJSON d'un itinéraire"""
    # Créer la carte centrée sur l'Île-de-France
    m = folium.Map(location=[48.8566, 2.3522], zoom_start=10)
    
    # Couleurs pour les différents types de trajets
    colors = {
        'rabattement': '#4CAF50',  # Vert pour rabattement (vélo)
        'diffusion': '#FF6B6B',    # Rouge pour diffusion (vélo)
        'transport': '#45B7D1'     # Bleu pour transport en commun
    }
    
    # Ajouter les marqueurs des points exacts d'origine et destination
    folium.Marker(
        [origin_coords[1], origin_coords[0]],  # lat, lon (inversion car origin_coords est en lon, lat)
        popup="🟢 Point de départ exact",
        icon=folium.Icon(color='green', icon='play')
    ).add_to(m)
    
    folium.Marker(
        [destination_coords[1], destination_coords[0]],  # lat, lon (inversion car destination_coords est en lon, lat)
        popup="🔴 Point d'arrivée exact",
        icon=folium.Icon(color='red', icon='stop')
    ).add_to(m)
    
    # Ajouter les géométries des gares (points plus petits)
    if 'geometry_ori' in route_data and route_data['geometry_ori']:
        geom_ori = parse_geojson_string(route_data['geometry_ori'])
        if geom_ori:
            folium.GeoJson(
                geom_ori,
                marker=folium.CircleMarker(radius=5, color='darkgreen', fill=True, popup="Gare d'origine")
            ).add_to(m)
    
    if 'geometry_dest' in route_data and route_data['geometry_dest']:
        geom_dest = parse_geojson_string(route_data['geometry_dest'])
        if geom_dest:
            folium.GeoJson(
                geom_dest,
                marker=folium.CircleMarker(radius=5, color='darkred', fill=True, popup="Gare de destination")
            ).add_to(m)
    
    # Ajouter le trajet de rabattement (pointillés)
    if 'rabattement_geometry' in route_data and route_data['rabattement_geometry']:
        rabattement_geom = parse_geojson_string(route_data['rabattement_geometry'])
        add_geojson_to_map(m, rabattement_geom, colors['rabattement'], "dashed", 4)
    
    # Ajouter le trajet de diffusion (pointillés)
    if 'diffusion_geometry' in route_data and route_data['diffusion_geometry']:
        diffusion_geom = parse_geojson_string(route_data['diffusion_geometry'])
        add_geojson_to_map(m, diffusion_geom, colors['diffusion'], "dashed", 4)
    
    # Ajouter les trajets en transport en commun (ligne continue)
    if 'geojson' in route_data and route_data['geojson']:
        transport_geom = parse_geojson_string(route_data['geojson'])
        if transport_geom:
            add_geojson_to_map(m, transport_geom, colors['transport'], "solid", 5)
    
    return m

def geocode_address(address):
    """Géocode une adresse en utilisant l'API Nominatim d'OpenStreetMap"""
    if not address.strip():
        return None, None
    
    try:
        # Ajouter "France" à la recherche pour améliorer la précision
        search_query = f"{address}, France"
        
        # URL de l'API Nominatim
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            'q': search_query,
            'format': 'json',
            'limit': 1,
            'countrycodes': 'fr',  # Limiter à la France
            'bounded': 1,
            'viewbox': '1.4,49.0,3.2,48.1'  # Bounding box approximative de l'Île-de-France
        }
        
        headers = {
            'User-Agent': 'StreamlitTransportApp/1.0'
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=5)
        response.raise_for_status()
        
        data = response.json()
        
        if data and len(data) > 0:
            lat = float(data[0]['lat'])
            lon = float(data[0]['lon'])
            return lat, lon
        else:
            return None, None
            
    except Exception as e:
        st.error(f"Erreur lors du géocodage de '{address}': {str(e)}")
        return None, None

def format_datetime_for_api(date, time):
    """Formate la date et l'heure pour l'API Navitia"""
    dt = datetime.combine(date, time)
    return dt.strftime("%Y%m%dT%H%M%S")

def main():
    st.title("🚲⚡️ Rayon d'Action")
    st.markdown("Trouvez le meilleur itinéraire combinant vélo et transport en commun en Île-de-France")
    
    # Sidebar pour les paramètres
    st.sidebar.header("⚙️ Paramètres de recherche")
    
    # Sélection des coordonnées
    st.sidebar.subheader("📍 Points de départ et d'arrivée")
    
    # Les coordonnées seront définies uniquement par géocodage d'adresses
    
    # Sélection par adresse
    with st.sidebar.expander("📮 Sélection par adresse", expanded=True):
        st.write("**Adresse de départ:**")
        origin_address = st.text_input(
            "Adresse de départ",
            placeholder="Ex: 12 rue de la Paix, Paris",
            key="origin_address_input"
        )
        
        if st.button("🔍 Géocoder départ", key="geocode_origin"):
            if origin_address:
                st.session_state.geocoding_in_progress = True
                with st.spinner("Géocodage en cours..."):
                    lat, lon = geocode_address(origin_address)
                    if lat and lon:
                        st.session_state.origin_lat = lat
                        st.session_state.origin_lon = lon
                        st.success(f"✅ Adresse trouvée: {lat:.4f}, {lon:.4f}")
                        # Nettoyer le flag et relancer
                        if 'geocoding_in_progress' in st.session_state:
                            del st.session_state.geocoding_in_progress
                        st.rerun()
                    else:
                        st.error("❌ Adresse non trouvée. Essayez une adresse plus précise.")
                        if 'geocoding_in_progress' in st.session_state:
                            del st.session_state.geocoding_in_progress
            else:
                st.warning("⚠️ Veuillez saisir une adresse")
        
        st.write("**Adresse de destination:**")
        dest_address = st.text_input(
            "Adresse de destination",
            placeholder="Ex: 5 avenue des Champs-Élysées, Paris",
            key="dest_address_input"
        )
        
        if st.button("🔍 Géocoder destination", key="geocode_dest"):
            if dest_address:
                st.session_state.geocoding_in_progress = True
                with st.spinner("Géocodage en cours..."):
                    lat, lon = geocode_address(dest_address)
                    if lat and lon:
                        st.session_state.dest_lat = lat
                        st.session_state.dest_lon = lon
                        st.success(f"✅ Adresse trouvée: {lat:.4f}, {lon:.4f}")
                        # Nettoyer le flag et relancer
                        if 'geocoding_in_progress' in st.session_state:
                            del st.session_state.geocoding_in_progress
                        st.rerun()
                    else:
                        st.error("❌ Adresse non trouvée. Essayez une adresse plus précise.")
                        if 'geocoding_in_progress' in st.session_state:
                            del st.session_state.geocoding_in_progress
            else:
                st.warning("⚠️ Veuillez saisir une adresse")
    

    
    # Vérifier que les coordonnées sont disponibles (géocodées)
    if ('origin_lat' not in st.session_state or 'origin_lon' not in st.session_state or
        'dest_lat' not in st.session_state or 'dest_lon' not in st.session_state):
        origin_coords = None
        destination_coords = None
    else:
        # Utiliser les coordonnées géocodées
        origin_coords = [st.session_state.origin_lat, st.session_state.origin_lon]
        destination_coords = [st.session_state.dest_lat, st.session_state.dest_lon]
    
    # Affichage des coordonnées actuelles
    st.sidebar.write("**Coordonnées actuelles:**")
    if origin_coords:
        st.sidebar.write(f"🟢 **Origine:** {origin_coords[0]:.4f}, {origin_coords[1]:.4f}")
    else:
        st.sidebar.write("🟢 **Origine:** Non définie - Veuillez géocoder une adresse")
    
    if destination_coords:
        st.sidebar.write(f"🔴 **Destination:** {destination_coords[0]:.4f}, {destination_coords[1]:.4f}")
    else:
        st.sidebar.write("🔴 **Destination:** Non définie - Veuillez géocoder une adresse")
    
    # Sélection de la date et de l'heure
    st.sidebar.subheader("📅 Date et heure de départ")
    
    departure_date = st.sidebar.date_input(
        "Date de départ",
        value=datetime.now().date(),
        min_value=datetime.now().date(),
        max_value=datetime.now().date() + timedelta(days=30)
    )
    
    departure_time = st.sidebar.time_input(
        "Heure de départ",
        value=datetime.now().time()
    )
    
    # Sélection du rayon
    st.sidebar.subheader("🔍 Rayon de recherche")
    radius_km = st.sidebar.slider(
        "Rayon de recherche (km)",
        min_value=0.5,
        max_value=10.0,
        value=5.0,
        step=0.5,
        help="Rayon de recherche des gares autour des points de départ et d'arrivée"
    )
    
    # Convertir en mètres
    radius_m = int(radius_km * 1000)
    
    # Bouton GO!
    if st.sidebar.button("🚀 GO! Calculer les itinéraires", type="primary"):
        if origin_coords and destination_coords:
            st.session_state.calculate = True
            st.session_state.origin_coords = (origin_coords[1], origin_coords[0])  # lon, lat
            st.session_state.destination_coords = (destination_coords[1], destination_coords[0])  # lon, lat
            st.session_state.datetime_str = format_datetime_for_api(departure_date, departure_time)
            st.session_state.radius = radius_m
        else:
            st.sidebar.error("⚠️ Veuillez d'abord géocoder les adresses de départ ET de destination !")
    
    # Zone principale
    if hasattr(st.session_state, 'calculate') and st.session_state.calculate:
        
        # Affichage des paramètres de recherche
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Origine", f"{st.session_state.origin_coords[1]:.4f}, {st.session_state.origin_coords[0]:.4f}")
        with col2:
            st.metric("Destination", f"{st.session_state.destination_coords[1]:.4f}, {st.session_state.destination_coords[0]:.4f}")
        with col3:
            st.metric("Rayon", f"{radius_km} km")
        
        # Barre de progression
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Initialiser l'optimiseur
            status_text.text("Initialisation de l'optimiseur...")
            progress_bar.progress(20)
            
            parquet_path = "data/emplacement-des-gares-idf.parquet"
            optimizer = RouteOptimizer(parquet_path=parquet_path)
            
            # Calculer les itinéraires
            status_text.text("Calcul des itinéraires...")
            progress_bar.progress(50)
            
            routes_df = optimizer.find_optimal_routes(
                origin_coords=st.session_state.origin_coords,
                destination_coords=st.session_state.destination_coords,
                buffer_radius=st.session_state.radius
            )
            
            progress_bar.progress(100)
            status_text.text("Calcul terminé!")
            
            if len(routes_df) > 0:
                st.success(f"✅ {len(routes_df)} itinéraires trouvés!")
                
                # Statistiques générales
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    avg_bike_dist = routes_df['distance_velo_totale'].mean()
                    st.metric("Distance vélo moyenne", f"{avg_bike_dist:.0f} m")
                with col2:
                    avg_bike_time = routes_df['duree_velo_totale'].mean()
                    st.metric("Temps vélo moyen", f"{avg_bike_time:.0f} min")
                with col3:
                    avg_total_time = routes_df['duree_totale_parcours'].mean()
                    st.metric("Temps total moyen", f"{avg_total_time:.0f} min")
                with col4:
                    best_time = routes_df['duree_totale_parcours'].min()
                    st.metric("Meilleur temps", f"{best_time:.0f} min")
                
                # Tableau des résultats
                st.subheader("📋 Itinéraires disponibles")
                
                # Préparer les données pour l'affichage
                display_df = routes_df.copy()
                display_df['Origine'] = display_df['nom_gares_ori']
                display_df['Destination'] = display_df['nom_gares_dest']
                display_df['Ligne(s)'] = display_df['ligne']
                display_df['Temps total (min)'] = display_df['duree_totale_parcours']
                display_df['Distance vélo (m)'] = display_df['distance_velo_totale']
                display_df['Temps vélo (min)'] = display_df['duree_velo_totale']
                
                # Trier par temps total croissant
                display_df = display_df.sort_values('duree_totale_parcours')
                
                # Sélection d'un itinéraire
                selected_columns = ['Origine', 'Destination', 'Ligne(s)', 'Temps total (min)', 
                                  'Distance vélo (m)', 'Temps vélo (min)']
                
                selected_idx = st.selectbox(
                    "Choisissez un itinéraire pour voir la carte détaillée:",
                    options=range(len(display_df)),
                    format_func=lambda x: f"#{x+1} - {display_df.iloc[x]['Origine']} → {display_df.iloc[x]['Destination']} - {display_df.iloc[x]['Temps total (min)']} min",
                    key="route_selector"
                )
                
                # Afficher le tableau
                st.dataframe(
                    display_df[selected_columns].reset_index(drop=True),
                    use_container_width=True
                )
                
                # Carte de l'itinéraire sélectionné
                if selected_idx is not None:
                    st.subheader(f"🗺️ Carte de l'itinéraire #{selected_idx+1}")
                    
                    selected_route = routes_df.iloc[selected_idx]
                    
                    # Informations détaillées de l'itinéraire
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.write("**Gare d'origine:**", selected_route['nom_gares_ori'])
                        st.write("**Mode:**", selected_route['mode_ori'])
                        if 'rabattement_distance' in selected_route:
                            st.write("**Distance rabattement:**", f"{selected_route['rabattement_distance']} m")
                    
                    with col2:
                        st.write("**Ligne(s):**", selected_route['ligne'])
                        if 'duree_traj' in selected_route:
                            st.write("**Durée transport:**", f"{selected_route['duree_traj']} min")
                    
                    with col3:
                        st.write("**Gare de destination:**", selected_route['nom_gares_dest'])
                        st.write("**Mode:**", selected_route['mode_dest'])
                        if 'diffusion_distance' in selected_route:
                            st.write("**Distance diffusion:**", f"{selected_route['diffusion_distance']} m")
                    
                    # Légende des couleurs
                    st.markdown("""
                    **Légende:**
                    - 🟢 **Vert (pointillés):** Trajet vélo de rabattement (origine → gare de départ)
                    - 🔵 **Bleu (continu):** Trajet en transport en commun
                    - 🔴 **Rouge (pointillés):** Trajet vélo de diffusion (gare d'arrivée → destination)
                    """)
                    
                    # Créer et afficher la carte
                    route_map = create_route_map(selected_route, st.session_state.origin_coords, st.session_state.destination_coords)
                    folium_static(route_map, width=1000, height=600)
                    
                    # Option de téléchargement des données
                    st.subheader("💾 Télécharger les résultats")
                    csv_data = routes_df.to_csv(index=False)
                    st.download_button(
                        label="Télécharger tous les itinéraires (CSV)",
                        data=csv_data,
                        file_name=f"itineraires_{departure_date.strftime('%Y%m%d')}_{departure_time.strftime('%H%M')}.csv",
                        mime="text/csv"
                    )
                
            else:
                st.warning("❌ Aucun itinéraire trouvé avec ces paramètres. Essayez d'augmenter le rayon de recherche.")
                
        except Exception as e:
            st.error(f"Erreur lors du calcul: {str(e)}")
            progress_bar.progress(0)
            status_text.text("")
    
    else:
        # Page d'accueil
        st.markdown("""
        ## Comment utiliser cette application ?
        
        1. **📍 Ajustez vos points de départ et d'arrivée** dans la barre latérale
        2. **📅 Choisissez votre date et heure de départ** 
        3. **🔍 Ajustez le rayon de recherche** des gares autour de vos points
        4. **🚀 Cliquez sur "GO!"** pour calculer les itinéraires
        5. **🗺️ Explorez les résultats** et visualisez les trajets sur la carte
        
        ### Fonctionnalités
        - ✅ Calcul d'itinéraires multimodaux (vélo + transport en commun)
        - ✅ Géocodage d'adresses automatique
        - ✅ Choix flexible de la date et de l'heure
        - ✅ Visualisation détaillée des trajets avec codes couleur
        - ✅ Téléchargement des résultats en CSV
        
        ### Légende des trajets
        - 🟢 **Vert pointillé**: Trajet vélo de rabattement 
        - 🔵 **Bleu continu**: Transport en commun
        - 🔴 **Rouge pointillé**: Trajet vélo de diffusion
        """)
        
        # Carte de prévisualisation avec les points sélectionnés
        if origin_coords and destination_coords:
            st.subheader("🗺️ Aperçu de vos points sélectionnés")
            
            # Créer une carte centrée entre les deux points
            center_lat = (origin_coords[0] + destination_coords[0]) / 2
            center_lon = (origin_coords[1] + destination_coords[1]) / 2
            
            preview_map = folium.Map(location=[center_lat, center_lon], zoom_start=9)
            
            # Ajouter les marqueurs
            folium.Marker(
                [origin_coords[0], origin_coords[1]], 
                popup=f"🟢 Origine<br>{origin_coords[0]:.4f}, {origin_coords[1]:.4f}", 
                icon=folium.Icon(color='green', icon='play')
            ).add_to(preview_map)
            
            folium.Marker(
                [destination_coords[0], destination_coords[1]], 
                popup=f"🔴 Destination<br>{destination_coords[0]:.4f}, {destination_coords[1]:.4f}", 
                icon=folium.Icon(color='red', icon='stop')
            ).add_to(preview_map)
            
            # Ajouter une ligne droite entre les points pour visualiser
            folium.PolyLine(
                locations=[[origin_coords[0], origin_coords[1]], [destination_coords[0], destination_coords[1]]],
                color='gray',
                weight=2,
                opacity=0.5,
                dash_array='10,10',
                popup='Distance à vol d\'oiseau'
            ).add_to(preview_map)
            
            # Afficher la carte
            folium_static(preview_map, width=700, height=400)
            
            # Informations sur la distance
            import math
            def haversine_distance(lat1, lon1, lat2, lon2):
                R = 6371  # Rayon de la Terre en km
                dlat = math.radians(lat2 - lat1)
                dlon = math.radians(lon2 - lon1)
                a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
                c = 2 * math.asin(math.sqrt(a))
                return R * c
            
            distance_km = haversine_distance(origin_coords[0], origin_coords[1], destination_coords[0], destination_coords[1])
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Distance à vol d'oiseau", f"{distance_km:.1f} km")
            with col2:
                st.metric("Rayon de recherche", f"{radius_km} km")

        else:
            st.info("📮 **Géocodez d'abord vos adresses de départ et de destination** pour voir un aperçu sur la carte.")

if __name__ == "__main__":
    main()