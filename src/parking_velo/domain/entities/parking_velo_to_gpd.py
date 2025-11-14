import geopandas as gpd
import pandas as pd
from shapely import wkb

GEO_POINT_COL = "geo_point_2d"
GEO_SHAPE_COL = "geo_shape"


def parking_velo_to_gpd(df: pd.DataFrame) -> gpd.GeoDataFrame:
    df_gpd = gpd.GeoDataFrame(
        df,
        geometry=df[GEO_POINT_COL].apply(wkb.loads),
        crs="EPSG:2154"
    )
    return df_gpd.drop(columns=[GEO_POINT_COL, GEO_SHAPE_COL])
