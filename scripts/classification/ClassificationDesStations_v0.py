import pandas as pd
import geopandas as gpd
import copy

# =============================================================================
#
# HANDY FUNCTIONS
#
# =============================================================================
def findClassesWithKMeans(populationsCoordinates, idealIndividuals):

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

# =============================================================================
#
# MAIN
#
# =============================================================================
if __name__ == "__main__":

    mainDB = gpd.read_parquet('../../data/enrich/final_table.gpq')

    columnsForClassification = ['facilite_acces_order', 'pct_amethyste', 'LGF_250m', 'n_lifts', 'moyenne_stairs', 'moyenne_meters', 'total_nb_etapes']
    populationsCoordinates = mainDB[columnsForClassification].fillna(0.)
    idealIndividuals = pd.DataFrame(columns=columnsForClassification,
                                    index=[1, 2, 3, 4, 5],
                                    data=[[5., 2., 3., 0., 15., 226., 1000.],
                                          [4., 2., 2., 1., 10., 124., 100.],
                                          [3., 2., 1., 2., 0., 0., 0.],
                                          [2., 5., 0., 4., 0., 0., 0.],
                                          [1., 9., 0., 18., 0., 0., 0.],
                                          ]
                                    )
    classesDict = findClassesWithKMeans(populationsCoordinates, idealIndividuals)

    for className, classContent in classesDict.items():
        print('Pour', className, ':', len(classContent['population']), 'stations')
        for indivID in classContent['population']:
            mainDB.at[indivID, 'class_id'] = int(className.split(' ')[1])

    mainDB.to_parquet('../../data/enrich/final_table_with_class.gbq')