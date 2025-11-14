from utils.job_runner import JobRunner
from utils.loader_local import LoaderLocal
from utils.writer_local import WriterLocal
import pandas as pd


class ValidationJob(JobRunner):
    """
    Job de traitement des validations du réseau ferré.

    Cette classe charge plusieurs fichiers Parquet contenant le nombre de validations
    par jour pour différents trimestres, calcule le total de validations par station (id_zdc),
    extrait le total pour la catégorie "Amethyste", puis calcule le pourcentage de validations
    Amethyste par rapport au total.
    """

    def __init__(self):
        """
        Initialise les chemins d’entrée (liste de fichiers Parquet) et le chemin de sortie.

        Attributes:
            in_path_list (list): Liste de chemins vers les fichiers Parquet bruts.
            out_path (str): Chemin du fichier Parquet final consolidé.
        """
        self.in_path_list = [
            "/home/onyxia/work/hackathon_mobilites_2025/data/raw/validations-reseau-ferre-nombre-validations-par-jour-2eme-trimestre.parquet",
            "/home/onyxia/work/hackathon_mobilites_2025/data/raw/validations-reseau-ferre-nombre-validations-par-jour-3eme-trimestre.parquet",
            "/home/onyxia/work/hackathon_mobilites_2025/data/raw/validations-reseau-ferre-nombre-validations-par-jour-2eme-trimestre.parquet"
        ]
        self.out_path = "/home/onyxia/work/hackathon_mobilites_2025/data/interim/validation_pourcentage.parquet"

    def process(self):
        """
        Exécute le pipeline complet de traitement des validations :

        1. Chargement de tous les fichiers Parquet bruts.
        2. Concatenation en un DataFrame unique.
        3. Nettoyage et conversion des colonnes numériques.
        4. Calcul du total de validations par station (id_zdc).
        5. Calcul du total de validations pour la catégorie "Amethyste".
        6. Fusion des totaux et calcul du pourcentage de validations Amethyste.
        7. Écriture du résultat final au format Parquet.
        """

        # 1. Chargement et concaténation de tous les fichiers
        dataframes = []
        for file_path in self.in_path_list:
            df = LoaderLocal.loader_parquet(file_path)
            dataframes.append(df)
        df_concat = pd.concat(dataframes, ignore_index=True)

        # 2. Nettoyage et conversion des colonnes en numériques
        #    - 'id_zdc' : conversion simple
        #    - 'nb_vald' : suppression des espaces et conversion
        df_concat['id_zdc'] = pd.to_numeric(df_concat['id_zdc'], errors='coerce')
        df_concat['nb_vald'] = pd.to_numeric(
            df_concat['nb_vald'].apply(lambda x: x.replace(' ', '') if isinstance(x, str) else x),
            errors='coerce'
        )

        # 3. Calcul du total de validations par station (id_zdc)
        df_total = df_concat.groupby('id_zdc', as_index=False).agg(
            total_validation=('nb_vald', 'sum')
        )

        # 4. Calcul du total de validations pour la catégorie "Amethyste"
        df_amethyste = df_concat[df_concat['categorie_titre'] == 'Amethyste'].groupby('id_zdc', as_index=False).agg(
            total_validation_amethyste=('nb_vald', 'sum')
        )

        # 5. Fusion des totaux par id_zdc
        df_final = pd.merge(df_total, df_amethyste, on='id_zdc', how='inner')

        # 6. Calcul du pourcentage de validations Amethyste
        df_final['total_validation_amethyste'] = df_final['total_validation_amethyste'].fillna(0)
        df_final['pct_amethyste'] = (df_final['total_validation_amethyste'] / df_final['total_validation']) * 100
        df_final['pct_amethyste'] = df_final['pct_amethyste'].round(4)

        # 7. Écriture du DataFrame final au format Parquet
        WriterLocal.write_parquet(df_final, self.out_path)
