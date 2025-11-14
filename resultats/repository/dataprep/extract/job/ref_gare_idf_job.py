from utils.job_runner import JobRunner
from utils.loader_local import LoaderLocal
from utils.transformation import Transformation
from utils.writer_local import WriterLocal


class RefGareIdfJob(JobRunner):
    """
    Job de préparation et de transformation du référentiel des gares d'Île-de-France.

    Cette classe :
    - charge les données brutes issues du fichier CSV,
    - nettoie et standardise le nom des stations,
    - extrait et reformate les coordonnées géographiques,
    - convertit le DataFrame en GeoDataFrame,
    - exporte le résultat en GeoParquet.
    """

    def __init__(self):
        """
        Initialise les chemins d’entrée et de sortie nécessaires au job.

        Attributes:
            in_path (str): Chemin du fichier source contenant les gares IDF.
            out_path (str): Chemin du fichier GeoParquet produit.
        """
        self.in_path = "/home/onyxia/work/hackathon_mobilites_2025/data/raw/emplacement-des-gares-idf.csv"
        self.out_path = "/home/onyxia/work/hackathon_mobilites_2025/data/interim/ref_gares.gpq"

    def process(self):
        """
        Exécute l'ensemble du pipeline de traitement :

        1. Lecture des données brutes CSV.
        2. Nettoyage des noms de stations via `Transformation.clean_name`.
        3. Sélection des colonnes pertinentes.
        4. Extraction des coordonnées depuis le champ geo_point_2d.
        5. Conversion du DataFrame en GeoDataFrame.
        6. Écriture finale au format GeoParquet.
        """

        # 1. Lecture des données brutes à partir du fichier CSV fourni
        df = LoaderLocal.loader_csv(self.in_path)

        # 2. Création d'une version nettoyée du nom des stations
        df["station_clean"] = df["nom_zda"].apply(Transformation.clean_name)

        # 3. Sélection des colonnes utiles pour le référentiel des gares
        cols = [
            "geo_point_2d",
            "id_ref_zdc",
            "id_ref_zda",
            "nom_zda",
            "station_clean",
            "res_com",
            "mode",
            "exploitant"
        ]
        df_selected = df[cols]

        # 4. Extraction des coordonnées géographiques :
        #    La colonne "geo_point_2d" contient une string "lat,lon"
        #    → on la découpe et on convertit en float.
        coords = df_selected["geo_point_2d"].str.split(",", expand=True)

        df_selected = df_selected.copy()
        df_selected["latitude"] = coords[0].astype(float)
        df_selected["longitude"] = coords[1].astype(float)

        # 5. Conversion en GeoDataFrame 
        gdf_final = Transformation.transform_geopandas(df_selected, "latitude", "longitude")

        # 6. Écriture du GeoDataFrame final en GeoParquet pour usage cartographique
        WriterLocal.write_geoparquet(gdf_final, self.out_path)
