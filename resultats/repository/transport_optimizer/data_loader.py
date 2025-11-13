import pyarrow.parquet as pq
import geopandas as gpd
from shapely import wkb
from config import SPATIAL_CONFIG


class GareDataLoader:    
    def __init__(self, parquet_path: str):
        self.parquet_path = parquet_path
    
    def load_gares(self, transport_modes=["TRAIN", "RER"]):            
        table = pq.read_table(
            self.parquet_path, 
            columns=["geo_point_2d", "nom_gares", "id_ref_zda", "mode"]
        )
        df_ref_arr = table.to_pandas()

        df_ref_arr["geometry"] = df_ref_arr["geo_point_2d"].apply(
            lambda x: wkb.loads(x) if x is not None else None
        )
        
        gdf = gpd.GeoDataFrame(
            df_ref_arr, 
            geometry="geometry", 
            crs=SPATIAL_CONFIG["source_crs"]
        ).to_crs(SPATIAL_CONFIG["projected_crs"])
        
        gdf.drop(columns=["geo_point_2d"], inplace=True)
        
        return gdf[gdf["mode"].isin(transport_modes)].copy()
 