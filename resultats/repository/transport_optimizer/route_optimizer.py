import pandas as pd
from data_loader import GareDataLoader
from spatial_service import SpatialService
from transport_apis import GeoveloClient, NavitiaClient
from config import DEFAULT_JOURNEY_CONFIG, setup_logger


class RouteOptimizer:
    def __init__(self, parquet_path, geovelo_api_key=None):
        self.logger = setup_logger("RouteOptimizer")
        self.data_loader = GareDataLoader(parquet_path)
        self.spatial_service = SpatialService()
        self.geovelo_client = GeoveloClient(geovelo_api_key)
        self.navitia_client = NavitiaClient()
        self.logger.info(f"RouteOptimizer initialisé avec {parquet_path}")

    def find_optimal_routes(
        self, origin_coords, destination_coords, buffer_radius=5000
    ):
        gdf_gares = self.data_loader.load_gares()

        origin_stations = self.spatial_service.find_gares_around_point(
            gdf_gares, origin_coords[0], origin_coords[1], buffer_radius
        )
        destination_stations = self.spatial_service.find_gares_around_point(
            gdf_gares, destination_coords[0], destination_coords[1], buffer_radius
        )

        self.logger.info(
            f"Gares d'origine trouvées: {len(origin_stations)} dans un rayon de {buffer_radius}m"
        )
        self.logger.info(
            f"Gares de destination trouvées: {len(destination_stations)} dans un rayon de {buffer_radius}m"
        )

        # Calculer d'abord tous les trajets vélo uniques pour éviter les doublons d'appels API
        self.logger.info("Calcul des itinéraires vélo uniques (rabattement et diffusion)...")
        bike_routes_cache = self._calculate_unique_bike_routes(
            origin_stations, destination_stations, origin_coords, destination_coords
        )

        # Créer toutes les combinaisons possibles
        combinations_df = self._create_station_combinations(
            origin_stations, destination_stations
        )
        combinations_df.drop_duplicates(inplace=True)
        self.logger.info(f"Combinaisons gare-à-gare créées: {len(combinations_df)}")

        # Ajouter les itinéraires vélo pré-calculés aux combinaisons
        self.logger.info("Association des itinéraires vélo aux combinaisons...")
        combinations_df = self._add_cached_bike_routes(
            combinations_df, bike_routes_cache
        )

        # Calculer les itinéraires transport en commun
        self.logger.info("Calcul des itinéraires en transport en commun...")
        combinations_df = self._add_public_transport_routes(combinations_df)
        self.logger.info(f"Itinéraires complets calculés: {len(combinations_df)}")

        # Convertir les géométries en GeoJSON à la fin des traitements
        self.logger.debug("Conversion des géométries en GeoJSON...")
        combinations_df = self.spatial_service.convert_geometries_to_geojson(
            combinations_df, geometry_columns=["geometry_ori", "geometry_dest"]
        )
        self.logger.debug("Géométries converties en GeoJSON")

        combinations_df = combinations_df.apply(
            lambda row: self.spatial_service.split_multiple_geojson(row), axis=1
        )

        # Ajouter les colonnes de somme des distances et durées vélo
        self.logger.debug("Calcul des totaux des distances et durées vélo...")
        combinations_df = self._add_bike_totals(combinations_df)

        sorted_routes_df = combinations_df.sort_values(
            by=["duree_totale_parcours"]
        ).reset_index(drop=True)
        max_rows = 5 if len(sorted_routes_df) >= 5 else len(sorted_routes_df)
        best_routes = sorted_routes_df.iloc[:max_rows]

        self.logger.info(f"{len(combinations_df)} itinéraires trouvés dont {len(best_routes)} retenus")

        return best_routes

    def _create_station_combinations(self, origin_stations, destination_stations):
        """Crée toutes les combinaisons origine-destination"""
        # Conversion en DataFrames normaux pour le merge
        df_origin = pd.DataFrame(origin_stations).add_suffix("_ori")
        df_destination = pd.DataFrame(destination_stations).add_suffix("_dest")

        # Produit cartésien
        combinations = df_origin.merge(df_destination, how="cross")

        return combinations

    def _calculate_unique_bike_routes(self, origin_stations, destination_stations, origin_coords, destination_coords):
        """Calcule tous les trajets vélo uniques pour éviter les doublons d'appels API"""
        bike_routes_cache = {}
        
        # Extraire les coordonnées uniques des gares d'origine
        unique_origin_coords = {}
        for _, station in origin_stations.iterrows():
            station_coords = self.spatial_service.get_coordinates_from_geometry(station["geometry"])
            unique_origin_coords[station["id_ref_zda"]] = station_coords
        
        # Extraire les coordonnées uniques des gares de destination
        unique_dest_coords = {}
        for _, station in destination_stations.iterrows():
            station_coords = self.spatial_service.get_coordinates_from_geometry(station["geometry"])
            unique_dest_coords[station["id_ref_zda"]] = station_coords
        
        # Calculer les trajets de rabattement uniques
        self.logger.debug(f"Calcul de {len(unique_origin_coords)} trajets de rabattement uniques...")
        for station_id, station_coords in unique_origin_coords.items():
            route = self.geovelo_client.get_route(origin_coords, station_coords)
            bike_routes_cache[f"rabattement_{station_id}"] = route
        
        # Calculer les trajets de diffusion uniques
        self.logger.debug(f"Calcul de {len(unique_dest_coords)} trajets de diffusion uniques...")
        for station_id, station_coords in unique_dest_coords.items():
            route = self.geovelo_client.get_route(station_coords, destination_coords)
            bike_routes_cache[f"diffusion_{station_id}"] = route
        
        total_api_calls = len(unique_origin_coords) + len(unique_dest_coords)
        self.logger.info(f"Trajets vélo calculés avec {total_api_calls} appels API uniques")
        
        return bike_routes_cache

    def _add_cached_bike_routes(self, df, bike_routes_cache):
        """Ajoute les trajets vélo pré-calculés aux combinaisons"""
        self.logger.debug(f"Association des trajets vélo à {len(df)} combinaisons...")
        results = []
        successful_routes = 0

        for idx, row in df.iterrows():
            # Récupérer les trajets pré-calculés
            rabattement = bike_routes_cache.get(f"rabattement_{row['id_ref_zda_ori']}")
            diffusion = bike_routes_cache.get(f"diffusion_{row['id_ref_zda_dest']}")

            # Ajouter les résultats à la ligne
            row_result = row.copy()
            if rabattement:
                row_result["rabattement_distance"] = rabattement["distance"]
                row_result["rabattement_duration"] = rabattement["duration"]
                row_result["rabattement_geometry"] = rabattement["geometry"]

            if diffusion:
                row_result["diffusion_distance"] = diffusion["distance"]
                row_result["diffusion_duration"] = diffusion["duration"]
                row_result["diffusion_geometry"] = diffusion["geometry"]

            if rabattement and diffusion:
                successful_routes += 1

            results.append(row_result)

        self.logger.info(
            f"Itinéraires vélo associés: {successful_routes}/{len(df)} complets"
        )
        return pd.DataFrame(results)

    def _add_public_transport_routes(self, df):
        """Ajoute les itinéraires en transport en commun"""
        datetime_str = DEFAULT_JOURNEY_CONFIG["datetime_str"]

        # Appliquer la requête Navitia à chaque ligne
        transport_results = df.apply(
            lambda row: self.navitia_client.get_journey(
                row["id_ref_zda_ori"], row["id_ref_zda_dest"], datetime_str
            ),
            axis=1,
        )

        # Ajouter les colonnes de résultat
        if not transport_results.empty:
            df = pd.concat([df, transport_results], axis=1)

        return df

    def _add_bike_totals(self, df):
        """Ajoute les colonnes de totaux des distances et durées vélo"""
        # Distance totale vélo (rabattement + diffusion)
        df["distance_velo_totale"] = df.get("rabattement_distance", 0).fillna(
            0
        ) + df.get("diffusion_distance", 0).fillna(0)

        # Durée totale vélo (rabattement + diffusion)
        df["duree_velo_totale"] = df.get("rabattement_duration", 0).fillna(0) + df.get(
            "diffusion_duration", 0
        ).fillna(0)

        # Durée totale du parcours (vélo + transport en commun)
        df["duree_totale_parcours"] = df.get("duree_velo_totale", 0).fillna(0) + df.get(
            "duree_traj", 0
        ).fillna(0)

        self.logger.info(
            f"Totaux calculés - Distance vélo moyenne: {df['distance_velo_totale'].mean():.0f}m, "
            f"Durée totale moyenne: {df['duree_totale_parcours'].mean():.1f}min"
        )

        return df
