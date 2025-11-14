import pandas as pd
import copy

from utils.job_runner import JobRunner
from utils.loader_local import LoaderLocal
from utils.writer_local import WriterLocal


class ClassificationStationsJob(JobRunner):
    
    def __init__(self):
        self.in_path = "/home/onyxia/work/hackathon_mobilites_2025/data/enrich/final_table.gpq"
        self.out_path = "/home/onyxia/work/hackathon_mobilites_2025/data/enrich/final_table_with_class.gpq"

    def findClassesWithKMeans(self, populationsCoordinates, idealIndividuals):
        classesDict = {}
        for classId in range(1, len(idealIndividuals)+1):
            className = f'Classe {classId}'
            classesDict[className] = {
                'population': [],
                'k-moyenne': idealIndividuals.iloc[classId-1, :].values,
            }

        classesKMeans = [b['k-moyenne'] for a, b in classesDict.items()]
        buffClassesDict = copy.deepcopy(classesDict)
        for className, classContent in buffClassesDict.items():
            classContent['population'] = []

        for individualName, individualCoordinates in populationsCoordinates.iterrows():
            individualDistances = [(individualCoordinates-k).T @ (individualCoordinates-k) for k in classesKMeans]
            matchingClass = individualDistances.index(min(individualDistances)) + 1
            buffClassesDict[f'Classe {matchingClass}']['population'] += [individualName]

        classesDict = buffClassesDict
        return classesDict

    def process(self):
        df_final = LoaderLocal.loader_geoparquet(self.in_path)

        columnsForClassification = ['facilite_acces_order', 'pct_amethyste', 'LGF_250m', 'n_lifts', 'moyenne_stairs', 'moyenne_meters', 'total_nb_etapes']
        populationsCoordinates = df_final[columnsForClassification].fillna(0.)
        idealIndividuals = pd.DataFrame(columns=columnsForClassification,
                                        index=[1, 2, 3, 4, 5],
                                        data=[[5., 2., 3., 0., 15., 226., 1000.],
                                              [4., 2., 2., 1., 10., 124., 100.],
                                              [3., 2., 1., 2., 0., 0., 0.],
                                              [2., 5., 0., 4., 0., 0., 0.],
                                              [1., 9., 0., 18., 0., 0., 0.],
                                              ]
                                        )
        classesDict = self.findClassesWithKMeans(populationsCoordinates, idealIndividuals)

        for className, classContent in classesDict.items():
            print('Pour', className, ':', len(classContent['population']), 'stations')
            for indivID in classContent['population']:
                df_final.at[indivID, 'class_id'] = int(className.split(' ')[1])

        WriterLocal.write_geoparquet(df_final, self.out_path)
