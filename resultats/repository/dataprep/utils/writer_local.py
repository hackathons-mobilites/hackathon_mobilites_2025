import pandas as pd
import geopandas as gpd


class WriterLocal:
    """
    Classe utilitaire pour écrire des fichiers de données localement
    (CSV, Parquet et GeoParquet).

    Fournit des méthodes statiques pour sauvegarder des DataFrames et GeoDataFrames
    dans différents formats avec une gestion d'erreurs homogène.
    """

    @staticmethod
    def write_csv(df: pd.DataFrame, file_path: str, sep: str = ";", index: bool = False) -> None:
        """
        Écrit un DataFrame pandas dans un fichier CSV local.

        Args:
            df (pd.DataFrame): Données à sauvegarder.
            file_path (str): Chemin du fichier de sortie (.csv).
            sep (str, optional): Caractère séparateur. Par défaut, ';'.
            index (bool, optional): Indique si l’index doit être écrit dans le fichier.
                                    Par défaut, False.

        Raises:
            ValueError: Si l'écriture échoue ou si l'objet fourni n'est pas un DataFrame.
        """
        try:
            if not isinstance(df, pd.DataFrame):
                raise ValueError("L'objet fourni n'est pas un DataFrame pandas.")

            df.to_csv(file_path, sep=sep, index=index, encoding="utf-8")
            print(f"✅ CSV écrit avec succès dans '{file_path}'")

        except Exception as e:
            raise ValueError(f"Erreur lors de l’écriture du fichier CSV '{file_path}' : {e}")

    @staticmethod
    def write_parquet(df: pd.DataFrame, file_path: str) -> None:
        """
        Écrit un DataFrame pandas dans un fichier Parquet local.

        Args:
            df (pd.DataFrame): Données à sauvegarder.
            file_path (str): Chemin du fichier de sortie (.parquet).

        Raises:
            ValueError: Si l'écriture échoue ou si l'objet fourni n'est pas un DataFrame.
        """
        try:
            if not isinstance(df, pd.DataFrame):
                raise ValueError("L'objet fourni n'est pas un DataFrame pandas.")

            df.to_parquet(file_path)
            print(f"✅ Parquet écrit avec succès dans '{file_path}'")

        except Exception as e:
            raise ValueError(f"Erreur lors de l’écriture du fichier Parquet '{file_path}' : {e}")

    @staticmethod
    def write_geoparquet(gdf: gpd.GeoDataFrame, file_path: str) -> None:
        """
        Écrit un GeoDataFrame GeoPandas dans un fichier GeoParquet local.

        Args:
            gdf (gpd.GeoDataFrame): Données géospatiales à sauvegarder.
            file_path (str): Chemin du fichier de sortie (.parquet).

        Raises:
            ValueError: Si l'écriture échoue ou si l'objet fourni n'est pas un GeoDataFrame.
        """
        try:
            if not isinstance(gdf, gpd.GeoDataFrame):
                raise ValueError("L'objet fourni n'est pas un GeoDataFrame GeoPandas.")

            gdf.to_parquet(file_path)
            print(f"✅ GeoParquet écrit avec succès dans '{file_path}'")

        except Exception as e:
            raise ValueError(f"Erreur lors de l’écriture du fichier GeoParquet '{file_path}' : {e}")
