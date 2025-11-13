import geopandas as gpd
from shapely.geometry import Point


def nearest_parking_velo(df_parking_velo: gpd.GeoDataFrame, point: Point) -> gpd.GeoSeries:
    min_idx = df_parking_velo.distance(point).idxmin()
    return df_parking_velo.loc[min_idx]
