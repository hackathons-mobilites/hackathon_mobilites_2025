import pandas as pd
import copy

from utils.job_runner import JobRunner
from utils.loader_local import LoaderLocal
from utils.writer_local import WriterLocal


class ClassificationStationsJob(JobRunner):
    """
    Job de classification des stations en différentes classes selon des métriques clés.

    Cette classe utilise une approche inspirée du K-Means avec des centres idéaux prédéfinis
    pour attribuer chaque station à une classe. Les métriques utilisées pour la classification incluent :
    - facilité d'accès (facilite_acces_order)
    - pourcentage Amethyste (pct_amethyste)
    - nombre d'établissements critiques à proximité (LGF_250m)
    - nombre d'ascenseurs (n_lifts)
    - métriques moyennes d'escalier (moyenne_stairs, moyenne_meters)
    - nombre total d'étapes de correspondance (total_nb_etapes)
    """

    def __init__(self):
        """
        Initialise les chemins d’entrée et de sortie du job.

        Attributes:
            in_path (str): Chemin du fichier GeoParquet enrichi contenant les stations.
            out_path (str): Chemin du fichier GeoParquet final avec les classes attribuées.
        """
        self.in_path = "/home/onyxia/work/hackathon_mobilites_2025/data/enrich/final_table.gpq"
        self.out_path = "/home/onyxia/work/hackathon_mobilites_2025/data/enrich/final_table_with_class.gpq"

    def findClassesWithKMeans(self, populationsCoordinates, idealIndividuals):
        """
        Attribue chaque station à la classe dont le centre idéal est le plus proche
        (approche inspirée de K-Means avec centres prédéfinis).

        Args:
            populationsCoordinates (pd.DataFrame): Coordonnées/métriques de toutes les stations.
            idealIndividuals (pd.DataFrame): Centres idéaux de chaque classe pour les métriques.

        Returns:
            dict: Dictionnaire contenant chaque classe avec les stations qui lui sont assignées
                  et le centre idéal correspondant.
        """
        # Initialisation des classes avec leurs centres idéaux
        classesDict = {}
        for classId in range(1, len(idealIndividuals)+1):
            className = f'Classe {classId}'
            classesDict[className] = {
                'population': [],
                'k-moyenne': idealIndividuals.iloc[classId-1, :].values,
            }

        # Extraction des centres pour le calcul des distances
        classesKMeans = [b['k-moyenne'] for a, b in classesDict.items()]

        # Préparation d'une copie du dictionnaire pour remplir les populations
        buffClassesDict = copy.deepcopy(classesDict)
        for className, classContent in buffClassesDict.items():
            classContent['population'] = []

        # Attribution de chaque station à la classe la plus proche
        for individualName, individualCoordinates in populationsCoordinates.iterrows():
            individualDistances = [(individualCoordinates - k).T @ (individualCoordinates - k) for k in classesKMeans]
            matchingClass = individualDistances.index(min(individualDistances)) + 1
            buffClassesDict[f'Classe {matchingClass}']['population'] += [individualName]

        classesDict = buffClassesDict
        return classesDict

    def process(self):
        """
        Exécute le pipeline de classification des stations :

        1. Chargement du GeoParquet enrichi contenant toutes les stations.
        2. Sélection des colonnes pertinentes pour la classification.
        3. Définition des centres idéaux des classes.
        4. Attribution des stations aux classes via `findClassesWithKMeans`.
        5. Mise à jour du DataFrame avec l'identifiant de classe.
        6. Écriture du GeoParquet final avec les classes attribuées.
        """

        # 1. Chargement des données enrichies
        df_final = LoaderLocal.loader_geoparquet(self.in_path)

        # 2. Colonnes utilisées pour la classification
        columnsForClassification = [
            'facilite_acces_order',
            'pct_amethyste',
            'LGF_250m',
            'n_lifts',
            'moyenne_stairs',
            'moyenne_meters',
            'total_nb_etapes'
        ]
        populationsCoordinates = df_final[columnsForClassification].fillna(0.)

        # 3. Définition des centres idéaux pour chaque classe
        idealIndividuals = pd.DataFrame(
            columns=columnsForClassification,
            index=[1, 2, 3, 4, 5],
            data=[
                [5., 2., 3., 0., 15., 226., 1000.],
                [4., 2., 2., 1., 10., 124., 100.],
                [3., 2., 1., 2., 0., 0., 0.],
                [2., 5., 0., 4., 0., 0., 0.],
                [1., 9., 0., 18., 0., 0., 0.]
            ]
        )

        # 4. Attribution des stations aux classes
        classesDict = self.findClassesWithKMeans(populationsCoordinates, idealIndividuals)

        # 5. Mise à jour du DataFrame avec l'identifiant de classe
        for className, classContent in classesDict.items():
            print('Pour', className, ':', len(classContent['population']), 'stations')
            for indivID in classContent['population']:
                df_final.at[indivID, 'class_id'] = int(className.split(' ')[1])

        # 6. Écriture du GeoParquet final avec les classes
        WriterLocal.write_geoparquet(df_final, self.out_path)
