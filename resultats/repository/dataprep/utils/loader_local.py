import pandas as pd
import geopandas as gpd


class LoaderLocal:
    """
    Classe utilitaire pour charger des fichiers de données locaux (CSV et GeoParquet).

    Cette classe fournit des méthodes statiques pour lire des fichiers tabulaires
    (CSV) et géospatiaux (GeoParquet).

    Exemple :
        df = LoaderLocal.loader_csv("data/mon_fichier.csv", sep=";")
        gdf = LoaderLocal.loader_geoparquet("data/mes_points.parquet")
    """

    @staticmethod
    def loader_csv(file_path: str, sep: str = ";") -> pd.DataFrame:
        """
        Charge un fichier CSV local dans un DataFrame pandas.

        Args:
            file_path (str): Chemin vers le fichier CSV.
            sep (str, optional): Caractère séparateur. Par défaut, ';'.

        Returns:
            pd.DataFrame: Données chargées depuis le fichier CSV.

        Raises:
            ValueError: Si le fichier ne peut pas être lu ou n'existe pas.
        """
        try:
            df = pd.read_csv(file_path, sep=sep)
            if not isinstance(df, pd.DataFrame):
                raise ValueError("Le fichier n'a pas pu être lu comme DataFrame.")
            return df
        except Exception as e:
            raise ValueError(f"Erreur lors de la lecture du fichier CSV '{file_path}' : {e}")

    @staticmethod
    def loader_parquet(file_path: str) -> pd.DataFrame:
        """
        Charge un fichier CSV local dans un DataFrame pandas.

        Args:
            file_path (str): Chemin vers le fichier parquet.

        Returns:
            pd.DataFrame: Données chargées depuis le fichier parquet.

        Raises:
            ValueError: Si le fichier ne peut pas être lu ou n'existe pas.
        """
        try:
            df = pd.read_parquet(file_path)
            if not isinstance(df, pd.DataFrame):
                raise ValueError("Le fichier n'a pas pu être lu comme DataFrame.")
            return df
        except Exception as e:
            raise ValueError(f"Erreur lors de la lecture du fichier parquet '{file_path}' : {e}")

    @staticmethod
    def loader_geoparquet(file_path: str) -> gpd.GeoDataFrame:
        """
        Charge un fichier GeoParquet local dans un GeoDataFrame GeoPandas.

        Args:
            file_path (str): Chemin vers le fichier GeoParquet.

        Returns:
            gpd.GeoDataFrame: Données géospatiales chargées.

        Raises:
            ValueError: Si le fichier ne peut pas être lu comme GeoDataFrame.
        """
        try:
            gdf = gpd.read_parquet(file_path)
            if not isinstance(gdf, gpd.GeoDataFrame):
                raise ValueError("Le fichier n'a pas pu être lu comme GeoDataFrame.")
            return gdf
        except Exception as e:
            raise ValueError(f"Erreur lors de la lecture du fichier GeoParquet '{file_path}' : {e}")
