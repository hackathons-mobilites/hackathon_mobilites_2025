import geopandas as gpd
from shapely.geometry import Point
import pandas as pd


class Transformation:
    """
    Classe regroupant les transformations génériques utilisées dans l'ensemble du projet.

    Cette classe fournit des méthodes utilitaires pour le nettoyage des chaînes de caractères
    et la conversion de DataFrames pandas en GeoDataFrames.
    """

    @staticmethod
    def clean_name(name: str) -> str:
        """
        Nettoie les noms de stations pour les harmoniser entre plusieurs référentiels.

        Supprime les espaces, les tirets, et met le texte en minuscules.
        Utile avant de réaliser des jointures sur des noms de stations.

        Args:
            name (str): Nom brut de la station.

        Returns:
            str: Nom nettoyé (sans espaces ni tirets, en minuscules).

        Raises:
            ValueError: Si la valeur fournie n'est pas une chaîne de caractères.
        """
        try:
            if not isinstance(name, str):
                raise ValueError(f"Le nom fourni n'est pas une chaîne de caractères : {name}")

            name = name.strip()            # supprime espaces au début/fin
            name = name.replace(" ", "")   # supprime espaces internes
            name = name.replace("-", "")   # supprime tirets
            name = name.lower()            # met en minuscules

            return name

        except Exception as e:
            raise ValueError(f"Erreur lors du nettoyage du nom '{name}' : {e}")

    @staticmethod
    def transform_geopandas(df: pd.DataFrame, latitude: str, longitude) -> gpd.GeoDataFrame:
        """
        Transforme un DataFrame pandas contenant une colonne latitude et longitude.

        Args:
            df (pd.DataFrame): DataFrame contenant les données à convertir.
            latitude (str): Nom de la colonne contenant la latitude.
            longitude (str): Nom de la colonne contenant la longitude.

        Returns:
            gpd.GeoDataFrame: DataFrame d'entrée converti en GeoDataFrame (EPSG:4326) avec : 
            - La colonne geometry est ajoutée.
            - Les colonnes latitude et longitude sont suppprimées.

        Raises:
            ValueError: Si la transformation échoue ou si les colonnes ne sont pas présentes.
        """
        try:
            if latitude not in df.columns:
                raise ValueError(f"La colonne '{latitude}' est absente du DataFrame.")
            if longitude not in df.columns:
                raise ValueError(f"La colonne '{longitude}' est absente du DataFrame.")

            # Création de la géométrie
            df["geometry"] = df.apply(lambda row: Point(row[longitude], row[latitude]), axis=1)

            gdf = gpd.GeoDataFrame(df, geometry="geometry", crs="EPSG:4326")
            return gdf

        except Exception as e:
            raise ValueError(f"Erreur lors de la conversion en GeoDataFrame : {e}")
