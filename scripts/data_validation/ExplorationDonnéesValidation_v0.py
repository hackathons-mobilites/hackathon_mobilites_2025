import os

import re

import pandas as pd
import numpy as np
import copy

from scipy import stats
from scipy.signal import savgol_filter

from datetime import datetime
from datetime import timedelta

import colorsys

import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rcParams['figure.max_open_warning'] = 300
mpl.rcParams['font.family'] = 'Parisine Office'

ratpColors = {
    'jadeGreen': '#00AA91',
    'aquaGreen': '#9BD2C8',
    'institutionalBlue': '#0A0082',
    'turquoiseBlue': '#00A0BE',
    'skyBlue': '#AFE1FA',
    'pineGreen': '#007D69',
    'simpleRed': '#EB3C37',
    'lightOrange': '#F0AA00',
    'goldYellow': '#F5D750',
    'lightPink' : '#EBA0C8',
    'aniseGreen': '#C8D741',
    'raspberryPink': '#D72864',
    'generalGray': '#D0D0D0',
    }
outlinesWidth = 1.75

lineColors = {
    'L1': '#FFBE00',
    'L2': '#0055C8',
    'L3': '#6E6E00',
    'L3bis': '#82C8E6',
    'L4': '#A0006E',
    'L5': '#FF5A00',
    'L6': '#82DC73',
    'L7': '#FF82B4',
    'L7bis': '#82DC73',
    'L8': '#D282BE',
    'L9': '#D2D200',
    'L10': '#DC9600',
    'L11': '#6E491E',
    'L12': '#00643C',
    'L13': '#82C8E6',
    'L14': '#640082',
    'RERA': '#FF1400',
    'RERB': '#3C91DC',
    }

ugCodeLinesRef = {
    '01': 'L1',
    '02': 'L2',
    '03': 'L3',
    '04': 'L4',
    '05': 'L5',
    '06': 'L6',
    '07': 'L7',
    '08': 'L8',
    '09': 'L9',
    '10': 'L10',
    '11': 'L11',
    '12': 'L12',
    '13': 'L13',
    '14': 'L13',
    '16': 'L3bis',
    '17': 'L7bis',
    '18': 'L14',
    '36': 'RERA',
    '37': 'RERA',
    '38': 'RERB',
    '46': 'RERA',
    '48': 'RERB',
    '91': 'RERB',
}

idfmColors = {
    'softBlue': '#70BCF7',
    'rebeccaPurple': '#4F358B',
    'brightPink': '#E7306A',
    'deepLavender': '#8D84BB',
    'slightGrey': '#C6CDD0',
    'strongGrey': '#555F61',
}

# =============================================================================
#
# HANDY FUNCTIONS
#
# =============================================================================
def createFolderTree(path):

    rootFolder, endFolder = os.path.split(path)

    if len(rootFolder) != 0:
        createFolderTree(rootFolder)

    if not os.path.isdir(path):
        os.mkdir(path)

    return

# =============================================================================
#
# COMMON PLOT FUNCTIONS
#
# =============================================================================
def findProperTicks(lowerLim, upperLim):

    correctingFactor = 0
    while upperLim <= 10:
        upperLim *= 10
        correctingFactor += 1

    upperTenPower = 1
    while upperLim/10**upperTenPower >= 10:
        upperTenPower += 1

    tenPowerReduction = 0
    allMajorTicks = np.linspace(0, 10**(upperTenPower+1), num=10**upperTenPower + 1)
    allMinorTicks = np.linspace(0, 10**(upperTenPower+1), num=4*10**upperTenPower + 1)
    while len(allMajorTicks[(allMajorTicks >= lowerLim) & (allMajorTicks <= upperLim)]) >= 11:
        tenPowerReduction += 1
        allMajorTicks = np.linspace(0, 10**(upperTenPower+1), num=10**(upperTenPower-tenPowerReduction) + 1)
        allMinorTicks = np.linspace(0, 10**(upperTenPower+1), num=4*10**(upperTenPower-tenPowerReduction) + 1)

    firstIdxToTake = len(allMajorTicks[allMajorTicks < lowerLim]) - 1 if len(allMajorTicks[allMajorTicks < lowerLim]) > 0 else 0
    firstValueToTake = allMajorTicks[firstIdxToTake]
    lastIdxToTake = len(allMajorTicks[allMajorTicks <= upperLim])
    lastValueToTake = allMajorTicks[lastIdxToTake]

    properMajorTicks = allMajorTicks[firstIdxToTake:lastIdxToTake+1]/10**correctingFactor
    if len(properMajorTicks) < 5:
        properMajorTicks = np.linspace(properMajorTicks[0], properMajorTicks[-1], num=2*len(properMajorTicks)-1)
    properMinorTicks = allMinorTicks[(allMinorTicks >= firstValueToTake) & (allMinorTicks <= lastValueToTake)]/10**correctingFactor
    if len(properMinorTicks) < 20:
        properMinorTicks = np.linspace(properMinorTicks[0], properMinorTicks[-1], num=2*len(properMinorTicks)-1)

    return properMajorTicks, properMinorTicks

def findAndExpandIntInStr(strWithInts):

    expandedStr = [k for k in strWithInts]

    intsPos = []
    for charIdx, char in enumerate(expandedStr):
        if char.isnumeric():
            intsPos += [charIdx]

    if len(intsPos) == 0:

        pass

    elif len(intsPos) > 1:

        firstPos = intsPos[0]
        secondPos = firstPos
        for firstIntIdx, secondIntIdx in zip(intsPos[:-1], intsPos[1:]):

            if secondIntIdx-firstIntIdx == 1:
                secondPos = secondIntIdx
            else:
                currInt = strWithInts[firstPos: secondPos+1]
                intToUse = f'{currInt:>06}'.replace(currInt, currInt[0])
                expandedStr[firstPos] = intToUse
                firstPos = secondIntIdx
                secondPos = firstPos

        currInt = strWithInts[firstPos: secondPos+1]
        intToUse = f'{currInt:>06}'.replace(currInt, currInt[0])
        expandedStr[firstPos] = intToUse

    else:

        expandedStr[intsPos[0]] = f'{strWithInts[intsPos[0]]:>06}'

    expandedStr = ''.join(expandedStr)

    return expandedStr

def shapeGenericAx(ax, sortLegend=True):

    ax.grid(visible=True, which='major', axis='both', linestyle='-', linewidth=0.3, color=idfmColors['deepLavender'], zorder=0.2,)
    ax.grid(visible=True, which='minor', axis='both', linestyle='-', linewidth=0.2, color=idfmColors['deepLavender'], zorder=0.2,)

    ax.tick_params(axis='x', colors=idfmColors['rebeccaPurple'], which='major', width=outlinesWidth)
    ax.tick_params(axis='x', colors=idfmColors['rebeccaPurple'], which='minor', width=0.)
    ax.xaxis.label.set_color(idfmColors['rebeccaPurple'])

    ax.tick_params(axis='y', colors=idfmColors['softBlue'], which='major', width=outlinesWidth)
    ax.tick_params(axis='y', colors=idfmColors['softBlue'], which='minor', width=0.)
    ax.yaxis.label.set_color(idfmColors['softBlue'])

    ax.spines['left'].set_color(idfmColors['softBlue'])
    ax.spines['left'].set_linewidth(outlinesWidth)
    ax.spines['bottom'].set_color(idfmColors['rebeccaPurple'])
    ax.spines['bottom'].set_linewidth(outlinesWidth)
    ax.spines['right'].set_color(idfmColors['rebeccaPurple'])
    ax.spines['right'].set_linewidth(outlinesWidth)
    ax.spines['top'].set_color(idfmColors['softBlue'])
    ax.spines['top'].set_linewidth(outlinesWidth)

    if len(ax.get_legend_handles_labels()[1]):

        legendLabels = ax.get_legend_handles_labels()[1]
        if sortLegend:
            legendLabels.sort(key=findAndExpandIntInStr)

        legendHandles = ax.get_legend_handles_labels()[0]
        correctHandlesOrder = [ax.get_legend_handles_labels()[1].index(k) for k in legendLabels]
        sortedLegendHandles = [legendHandles[k] for k in correctHandlesOrder]

        if len(ax.get_legend_handles_labels()[1]) <= 6:

            ncol = 2 if len(ax.get_legend_handles_labels()[1]) > 3 else 1

            ax.legend(handles=sortedLegendHandles,
                      labels=legendLabels,
                      fontsize=7.,
                      labelcolor=idfmColors['softBlue'],
                      edgecolor=idfmColors['rebeccaPurple'],
                      ncol=ncol,
                      )

        else:

            ncol = 1 if len(legendLabels) <= 20 else 2
            locToUse = 'upper left'
            bboxToUse = (1., 1.)

            ax.legend(handles=sortedLegendHandles,
                      labels=legendLabels,
                      fontsize=7.,
                      labelcolor=idfmColors['softBlue'],
                      frameon=False, ncol=ncol,
                      loc=locToUse, bbox_to_anchor=bboxToUse,
                      )

    return ax


# =============================================================================
#
# DATA VIZ
#
# =============================================================================
def plotTopXStationPerTrafic(structuredData, **kwargs):

    if 'mainColor' in kwargs.keys():
        mainColor = kwargs['mainColor']
    else:
        mainColor = idfmColors['brightPink']

    if 'titleCategory' in kwargs.keys():
        titleCategory = kwargs['titleCategory']
    else:
        titleCategory = 'Validations Amethyste'

    if 'topX' in kwargs.keys():
        topX = kwargs['topX']
    else:
        topX = 10

    if 'proportionedData' in kwargs.keys():
        proportionedData = kwargs['proportionedData']
    else:
        proportionedData = False

    if 'ascendingSort' in kwargs.keys():
        ascendingSort = kwargs['ascendingSort']
    else:
        ascendingSort = False

    chosenDPI = 125
    tightLayoutRect = {'rect':(0.0,0.0,0.995,0.995)}
    figWidth, figHeight = 1000, 800

    fig, ax = plt.subplots(figsize=(figWidth/chosenDPI,figHeight/chosenDPI),
                           dpi=chosenDPI)
    fig.set_tight_layout(tightLayoutRect)

    sortedData = structuredData[titleCategory].sort_values(ascending=ascendingSort)
    topXData = sortedData[:topX]

    for stationIdx, specStation in enumerate(topXData.index):

        ax.bar(stationIdx,
               topXData[specStation],
               width=0.5,
               color=mainColor,
               edgecolor='#FFFFFF',
               linewidth=0.5,
               zorder=2.1,
               )

    ax.set_xticks([k for k in range(len(topXData.index))],
                  labels=topXData.index,
                  minor=False,
                  fontsize=14,
                  ha='right', va='top',
                  rotation=45,
                  )
    ax.set_xlim(-0.5, len(topXData.index)-0.5)

    dataType = 'Total' if not proportionedData else 'Part (%)'
    majorYTicks, minorYTicks = findProperTicks(0., topXData.max())
    ax.set_yticks(majorYTicks,
                  minor=False,
                  )
    ax.set_yticks(minorYTicks,
                  minor=True,
                  )
    ax.set_ylabel(f'{titleCategory} - {dataType} par an',
                  stretch='condensed',
                  fontsize=18, fontweight='bold',
                  )
    ax.set_ylim(majorYTicks[0], majorYTicks[-1])

    ax = shapeGenericAx(ax)

    ax.grid(visible=False, which='major', axis='x')
    ax.grid(visible=True, which='minor', axis='x', linestyle='-', linewidth=0.25, color=ratpColors['aquaGreen'], zorder=0.5,)

    folderPath = 'Graphs/'
    createFolderTree(folderPath)
    plotName = f'Total {titleCategory} par an' if not proportionedData else f'Part de {titleCategory} par an'
    fig.savefig(f"{folderPath}/{plotName}.png", transparent=False)

    return

# =============================================================================
#
# MAIN
#
# =============================================================================
if __name__ == "__main__":

    print('Fichier créé le', datetime.now().strftime('%d/%m/%Y'), 'à', datetime.now().strftime('%H:%M:%S'))
    print('Auteur : Erwann YVIN (EY758671)')

    # Pour l'encoding des données de validation en .csv : utf_16_be

    validationData = pd.DataFrame()
    validationFiles = [k for k in os.listdir('datasets') if k.endswith('.parquet') and 'validations-reseau-ferre' in k]
    for specFile in validationFiles:
        specFileData = pd.read_parquet(specFile, engine='fastparquet')
        validationData = pd.concat([validationData, specFileData], axis='index')

    uniqueStations = validationData['libelle_arret'].unique().tolist()
    structuredColumns = [f'Validations {k}' for k in np.unique(validationData['categorie_titre'])]
    structuredValidationData = pd.DataFrame(columns=['Station ID'] + structuredColumns)

#    for specStation in uniqueStations:
#
#        stationIDA = validationData[validationData['libelle_arret'] == specStation]['ida'].dropna().unique()
#        uniqueIDA = np.unique([float(k.replace(' ', '')) if type(k) is str else k for k in stationIDA]).tolist()
#
#        stationID_ZDC = validationData[validationData['libelle_arret'] == specStation]['id_zdc'].dropna().unique()
#        uniqueID_ZDC = np.unique([float(k.replace(' ', '')) if type(k) is str else k for k in stationID_ZDC]).tolist()
#
#        uniqueID = np.unique(uniqueIDA + uniqueID_ZDC).tolist()[0]
#
#        structuredValidationData.at[specStation, 'Station ID'] = uniqueID
#
#        specStationData = validationData[validationData['libelle_arret'] == specStation]
#
#        for specValidation in structuredColumns:
#
#            validationCategory = ' '.join(specValidation.split(' ')[1:])
#            specValidationDataForStation = specStationData[specStationData['categorie_titre'] == validationCategory]
#            correctValidationValues = [float(k.replace(' ', '')) if type(k) is str else k for k in specValidationDataForStation['nb_vald'].values]
#            structuredValidationData.at[specStation, specValidation] = np.sum(correctValidationValues)
#
#    structuredValidationData.to_csv('datasets/Données de validation - Total annuel par forfait.csv')

    structuredValidationData = pd.read_csv('datasets/Données de validation - Total annuel par forfait.csv', index_col=0)
    plotTopXStationPerTrafic(structuredValidationData)

    proportionedData = 100*(structuredValidationData.T/structuredValidationData.T.sum()).T
    plotTopXStationPerTrafic(proportionedData, proportionedData=True)

#    for specStation in proportionedData.index:
#
#        stationIDA = validationData[validationData['libelle_arret'] == specStation]['ida'].dropna().unique()
#        uniqueIDA = np.unique([float(k.replace(' ', '')) if type(k) is str else k for k in stationIDA]).tolist()
#
#        stationID_ZDC = validationData[validationData['libelle_arret'] == specStation]['id_zdc'].dropna().unique()
#        uniqueID_ZDC = np.unique([float(k.replace(' ', '')) if type(k) is str else k for k in stationID_ZDC]).tolist()
#
#        uniqueID = np.unique(uniqueIDA + uniqueID_ZDC).tolist()[0]
#
#        proportionedData.at[specStation, 'Station ID'] = uniqueID
#
#    proportionedData[['Station ID'] + [k for k in proportionedData.columns if k != 'Station ID']].to_csv('datasets/Données de validation - Part annuelle de chaque forfait.csv')