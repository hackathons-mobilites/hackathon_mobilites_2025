from utils.job_runner import JobRunner
from utils.loader_local import LoaderLocal
from utils.writer_local import WriterLocal
from utils.transformation import Transformation
import pandas as pd


class EtablissementJob(JobRunner):
    """
    Job de préparation et de consolidation des données d'établissements
    (adultes handicapés, enfants handicapés, établissements hospitaliers).

    Cette classe charge plusieurs fichiers source hétérogènes, 
    extrait et normalise les colonnes essentielles (coordonnées + raison sociale),
    enrichit les données avec un type d'établissement, puis
    génère un GeoDataFrame exploitable pour cartographie.
    """

    def __init__(self):
        """
        Initialise les chemins d’entrée des trois sources de données ainsi que
        le chemin de sortie du fichier GeoParquet consolidé.

        Attributes:
            in_dico (dict): Dictionnaire associant chaque type d’établissement
                            à son fichier CSV brut.
            out_path (str): Chemin du fichier GeoParquet généré.
        """
        self.in_dico = {
            'Etablissements adultes handicapés':
                '/home/onyxia/work/hackathon_mobilites_2025/data/raw/etablissements_et_services_pour_adultes_handicapes.csv',
            'Etablissements enfants handicapés':
                '/home/onyxia/work/hackathon_mobilites_2025/data/raw/etablissements_et_services_pour_l_enfance_et_la_jeunesse_handicapee.csv',
            'Etablissements hospitaliers':
                '/home/onyxia/work/hackathon_mobilites_2025/data/raw/les_etablissements_hospitaliers_franciliens.csv'
        }

        self.out_path = "/home/onyxia/work/hackathon_mobilites_2025/data/interim/etablissements.gpq"

    def find_col(self, df_cols, candidates):
        """
        Recherche une colonne dans un DataFrame parmi une liste de noms possibles.

        Args:
            df_cols (iterable): Liste ou Index des colonnes du DataFrame.
            candidates (list): Liste de noms de colonnes possibles.

        Returns:
            str or None: Le nom de la première colonne trouvée, sinon None.
        """
        for cand in candidates:
            if cand in df_cols:
                return cand
        return None

    def prepare_df(self, df, type_etablissement):
        """
        Prépare un DataFrame provenant d’une source hétérogène afin d'en extraire :
        - les coordonnées géographiques (lat, lng)
        - la raison sociale
        - un tag précisant le type d’établissement

        Cette méthode harmonise la structure des données malgré les variations
        de noms de colonnes entre fichiers.

        Args:
            df (pd.DataFrame): Données brutes de l’établissement.
            type_etablissement (str): Libellé du type d’établissement.

        Returns:
            pd.DataFrame or None: Un DataFrame normalisé ou None si colonnes manquantes.
        """

        # Définition des correspondances possibles pour les colonnes à extraire
        col_map = {
            'lat': ['lat', 'LAT'],
            'lng': ['lng', 'LNG'],
            'RAISON_SOCIALE': ['RAISON_SOCIALE']
        }

        # Recherche automatique des colonnes compatibles dans le DataFrame
        lat_col = self.find_col(df.columns, col_map['lat'])
        lng_col = self.find_col(df.columns, col_map['lng'])
        rs_col = self.find_col(df.columns, col_map['RAISON_SOCIALE'])

        # Vérification de la présence des colonnes indispensables
        if not all([lat_col, lng_col, rs_col]):
            print(f"Colonnes manquantes dans {type_etablissement}")
            return None

        # Extraction et homogénéisation des noms de colonnes
        subset = df[[lat_col, lng_col, rs_col]].copy()
        subset.rename(columns={
            lat_col: 'lat',
            lng_col: 'lng',
            rs_col: 'raison_social'
        }, inplace=True)

        # Suppression des lignes sans coordonnées
        subset.dropna(subset=['lat', 'lng'], inplace=True)

        # Ajout du type d’établissement
        subset['type_etablissement'] = type_etablissement

        return subset

    def process(self):
        """
        Exécute le pipeline complet :

        1. Chargement des trois sources CSV.
        2. Extraction, normalisation et mise en cohérence des colonnes utiles.
        3. Fusion des jeux de données.
        4. Conversion en GeoDataFrame via Transformation.
        5. Export final en GeoParquet.

        Raises:
            ValueError: Si aucun DataFrame valide n’a pu être généré.
        """

        dataframes = []

        # Parcours de chaque type d’établissement et préparation de son DataFrame
        for type_etablissement, filepath in self.in_dico.items():
            df = LoaderLocal.loader_csv(filepath)
            subset = self.prepare_df(df, type_etablissement)
            if subset is not None:
                dataframes.append(subset)
        
        # Vérification que des données exploitables ont été générées
        if not dataframes:
            raise ValueError("Aucun DataFrame valide n'a été créé.")

        # Fusion de l'ensemble des établissements dans un DataFrame unique
        df_global = pd.concat(dataframes, ignore_index=True)

        # Conversion en GeoDataFrame avec géométrie basée sur lat/lng
        final_gdf = Transformation.transform_geopandas(df_global, "lat", "lng")

        # Export des données consolidées au format GeoParquet
        WriterLocal.write_geoparquet(final_gdf, self.out_path)
