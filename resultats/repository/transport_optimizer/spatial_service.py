import geopandas as gpd
import json
from shapely.geometry import Point, mapping
from config import SPATIAL_CONFIG


class SpatialService:    
    @staticmethod
    def find_gares_around_point(gdf_gares, longitude, latitude, buffer_radius=None):
        """
        Trouve les gares dans un rayon autour d'un point
        Args:
            longitude: Longitude du point central (WGS84)
            latitude: Latitude du point central (WGS84)            
        Returns:
            GeoDataFrame: Gares trouvées avec géométries en WGS84
        """
        if buffer_radius is None:
            buffer_radius = SPATIAL_CONFIG["default_buffer_radius"]
        
        # Créer le point central
        center = Point(longitude, latitude)
        center_gdf = gpd.GeoDataFrame(
            [1], 
            geometry=[center], 
            crs=SPATIAL_CONFIG["source_crs"]
        ).to_crs(SPATIAL_CONFIG["projected_crs"])

        # Créer le buffer
        gdf_center_buffered = center_gdf.copy()
        gdf_center_buffered["geometry"] = center_gdf.geometry.buffer(buffer_radius)

        # Intersection spatiale
        spatial_joined = gpd.sjoin(gdf_center_buffered, gdf_gares, how="inner")
        spatial_joined.drop(columns=[0, "geometry"], inplace=True)

        # Récupérer les géométries originales
        geometries_gares = gdf_gares.loc[spatial_joined["index_right"], "geometry"]
        gares_avec_geometries = spatial_joined.copy()
        gares_avec_geometries["geometry"] = geometries_gares.values
        
        # Créer le GeoDataFrame final et reprojeter en WGS84
        result = gpd.GeoDataFrame(
            gares_avec_geometries, 
            geometry="geometry", 
            crs=gdf_gares.crs
        ).to_crs(SPATIAL_CONFIG["source_crs"])

        return result[["nom_gares", "id_ref_zda", "mode", "geometry"]]

    @staticmethod
    def get_coordinates_from_geometry(geometry):
        """Récupère les coordonnées lon, lat d'une géométrie Point"""
        return geometry.x, geometry.y
    
    @staticmethod
    def convert_geometries_to_geojson(df, geometry_columns=None):
        result_df = df.copy()

        for col in geometry_columns:
            if col in result_df.columns:
                result_df[col] = result_df[col].apply(
                    lambda geom: json.dumps(mapping(geom), separators=(',', ':')) if geom is not None else None
                )
        
        return result_df

    @staticmethod
    def split_multiple_geojson(row):
        r = row.copy()
        features = []
        for s in r["geojson"]:
            gj = json.loads(s)
            features.append({
                "type": "Feature",
                "geometry": {
                    "type": gj["type"],
                    "coordinates": gj["coordinates"],
                },
                "properties": gj.get("properties", {})
            })

        merged_geojson = {
            "type": "FeatureCollection",
            "features": features
        }
        r["geojson"] = merged_geojson
        return r