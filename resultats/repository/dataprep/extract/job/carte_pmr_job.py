from utils.job_runner import JobRunner
from utils.loader_local import LoaderLocal
from utils.transformation import Transformation
from utils.writer_local import WriterLocal


class CartePmrJob(JobRunner):
    """
    Job de traitement des données liées à l’accessibilité PMR des stations.

    Cette classe hérite de `JobRunner` et implémente la méthode `process()`
    pour effectuer un flux complet de traitement :
    - Chargement des données brutes
    - Nettoyage et transformation
    - Génération de colonnes dérivées
    - Export au format Parquet
    """

    def __init__(self):
        """
        Initialise les chemins d’entrée et de sortie nécessaires au job.

        Attributes:
            in_path (str): Chemin vers le fichier CSV brut contenant les données PMR.
            out_path (str): Chemin de sortie pour enregistrer les données transformées.
        """
        self.in_path = "/home/onyxia/work/hackathon_mobilites_2025/data/raw/carte_pmr.csv"
        self.out_path = "/home/onyxia/work/hackathon_mobilites_2025/data/interim/carte_pmr.parquet"

    def process(self):
        """
        Exécution complète du pipeline de traitement des données PMR.

        Étapes principales :
        1. Lecture du fichier CSV brut.
        2. Nettoyage du nom des stations.
        3. Sélection des colonnes pertinentes.
        4. Conversion d'un code couleur en valeur numérique ordonnée.
        5. Enregistrement du résultat final au format Parquet.
        """

        # 1. Lecture des données brutes à partir d'un fichier CSV local
        df = LoaderLocal.loader_csv(self.in_path)
       
        # 2. Nettoyage du nom des stations 
        df["station_clean"] = df["station"].apply(Transformation.clean_name)

        # 3. Sélection des colonnes nécessaires à l'analyse
        cols = [
            "ligne",
            "station",
            "facilite_acces_code",
            "facilite_acces",
            "nombre_facilite_acces_station",
            "station_clean"
        ]
        df_final = df[cols]

        # 4. Création d'un mapping pour convertir les codes couleur en ordre numérique.
        color_map = {
            'green': 1,
            'black': 2,
            'yellow': 3,
            'white': 4,
            'grey': 5
        }

        # 5. Application du mapping pour générer une nouvelle colonne d’ordre d’accessibilité
        df_final['facilite_acces_order'] = df_final['facilite_acces_code'].map(color_map)
        
        # 6. Écriture des données transformées au format Parquet dans le dossier prévu
        WriterLocal.write_parquet(df_final, self.out_path)
