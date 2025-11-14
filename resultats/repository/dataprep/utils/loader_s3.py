import boto3
import pandas as pd
import geopandas as gpd


class LoaderS3:
    """
    Classe utilitaire pour charger des fichiers stockés sur un bucket S3 (MinIO).

    Cette classe permet de lire des fichiers CSV, Parquet et GeoParquet directement
    depuis un espace S3 sécurisé en utilisant les identifiants d’accès fournis.

    Exemple :
        loader = LoaderS3(access_key, secret_key, session_token)
        df = loader.loader_csv("path/to/file.csv", sep=";")
        gdf = loader.loader_geoparquet("path/to/file.parquet")
    """

    def __init__(self, access_key: str, secret_key: str, session_token: str):
        """
        Initialise le client S3 avec les identifiants d’accès et les paramètres du bucket.

        Args:
            access_key (str): Clé d'accès AWS.
            secret_key (str): Clé secrète AWS.
            session_token (str): Jeton de session AWS temporaire.
        """
        self.access_key = access_key
        self.secret_key = secret_key
        self.session_token = session_token
        self.region = "fr-central"
        self.endpoint_url = "https://minio.data-platform-self-service.net"
        self.bucket = "dlb-hackathon"

        # Création du client S3
        self.s3_client = boto3.client(
            "s3",
            endpoint_url=self.endpoint_url,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            aws_session_token=self.session_token,
            region_name=self.region,
        )

    def loader_csv(self, file_path: str, sep: str = ";") -> pd.DataFrame:
        """
        Charge un fichier CSV depuis un bucket S3 dans un DataFrame pandas.

        Args:
            file_path (str): Chemin du fichier dans le bucket S3.
            sep (str, optional): Caractère séparateur du CSV. Par défaut, ';'.

        Returns:
            pd.DataFrame: Données chargées depuis le fichier CSV.

        Raises:
            ValueError: Si la lecture du fichier échoue ou si le code HTTP n'est pas 200.
        """
        try:
            response = self.s3_client.get_object(Bucket=self.bucket, Key=file_path)
            status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")

            if status != 200:
                raise ValueError(
                    f"Erreur HTTP {status} lors de la récupération du fichier '{file_path}'.")

            df = pd.read_csv(response.get("Body"), sep=sep)
            if not isinstance(df, pd.DataFrame):
                raise ValueError("Le fichier n'a pas pu être lu comme DataFrame.")

            return df

        except Exception as e:
            raise ValueError(
                f"Erreur lors de la lecture du fichier CSV '{file_path}' depuis S3 : {e}")

    def loader_parquet(self, file_path: str) -> pd.DataFrame:
        """
        Charge un fichier Parquet depuis un bucket S3 dans un DataFrame pandas.

        Args:
            file_path (str): Chemin du fichier dans le bucket S3.

        Returns:
            pd.DataFrame: Données chargées depuis le fichier Parquet.

        Raises:
            ValueError: Si la lecture du fichier échoue ou si le code HTTP n'est pas 200.
        """
        try:
            response = self.s3_client.get_object(Bucket=self.bucket, Key=file_path)
            status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")

            if status != 200:
                raise ValueError(
                    f"Erreur HTTP {status} lors de la récupération du fichier '{file_path}'.")

            df = pd.read_parquet(response.get("Body"))
            if not isinstance(df, pd.DataFrame):
                raise ValueError("Le fichier n'a pas pu être lu comme DataFrame.")

            return df

        except Exception as e:
            raise ValueError(
                f"Erreur lors de la lecture du fichier Parquet '{file_path}' depuis S3 : {e}")

    def loader_geoparquet(self, file_path: str) -> gpd.GeoDataFrame:
        """
        Charge un fichier GeoParquet depuis un bucket S3 dans un GeoDataFrame GeoPandas.

        Args:
            file_path (str): Chemin du fichier dans le bucket S3.

        Returns:
            gpd.GeoDataFrame: Données géospatiales chargées depuis le fichier.

        Raises:
            ValueError: Si la lecture du fichier échoue ou si le code HTTP n'est pas 200.
        """
        try:
            response = self.s3_client.get_object(Bucket=self.bucket, Key=file_path)
            status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")

            if status != 200:
                raise ValueError(
                    f"Erreur HTTP {status} lors de la récupération du fichier '{file_path}'.")

            gdf = gpd.read_parquet(response.get("Body"))
            if not isinstance(gdf, gpd.GeoDataFrame):
                raise ValueError("Le fichier n'a pas pu être lu comme GeoDataFrame.")

            return gdf

        except Exception as e:
            raise ValueError(
                f"Erreur lors de la lecture du fichier GeoParquet '{file_path}' depuis S3 : {e}")
