##################################
#
#  Import et analyse des données
#
##################################

import requests
import pandas as pd
import numpy as np
import geopandas as gpd
import requests
import json
import csv
from datetime import datetime
from simpledbf import Dbf5

# fonction pour exporter les données de l'API Velib


def export_data_velib():
    """Convert Velib JSON data to CSV format"""
    url = "https://velib-metropole-opendata.smovengo.cloud/opendata/Velib_Metropole/station_status.json"
    # Fetch the JSON data
    response = requests.get(url)
    data = response.json()
    stations = data['data']['stations']
    # Define CSV file
    csv_file = path + '/velib_stations.csv'
    # Define headers
    headers = [
        'station_id',
        'station_code',
        'num_bikes_available',
        'mechanical_bikes',
        'ebikes',
        'num_docks_available',
        'is_installed',
        'is_returning',
        'is_renting',
        'last_reported',
        'last_reported_datetime'
    ]
    # Write to CSV
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for station in stations:
            # Extract bike types
            bike_types = station.get('num_bikes_available_types', [])
            mechanical = 0
            ebike = 0
            for bike_type in bike_types:
                if 'mechanical' in bike_type:
                    mechanical = bike_type['mechanical']
                if 'ebike' in bike_type:
                    ebike = bike_type['ebike']
            # Convert timestamp to datetime
            timestamp = station.get('last_reported', 0)
            dt_string = datetime.fromtimestamp(
                timestamp).isoformat() if timestamp else ''
            # Write row
            writer.writerow({
                'station_id': station.get('station_id'),
                'station_code': station.get('stationCode'),
                'num_bikes_available': station.get('num_bikes_available', 0),
                'mechanical_bikes': mechanical,
                'ebikes': ebike,
                'num_docks_available': station.get('num_docks_available', 0),
                'is_installed': station.get('is_installed', 0),
                'is_returning': station.get('is_returning', 0),
                'is_renting': station.get('is_renting', 0),
                'last_reported': timestamp,
                'last_reported_datetime': dt_string
            })
    print(f"CSV file saved to {csv_file}")
    print(f"Total stations: {len(stations)}")


path = "C:/Users/9606423P/SNCF/Datalab' Mass Transit GrpO365 - Documents/Rayonnement/Datathon/2025/Hackathon_2025/Donnees"

##### VELIB ######

export_data_velib()
referentiel_velib = pd.read_csv(
    path + '/Referentiel/velib_avec_uic.dbf.csv', sep=';')
data_velib = pd.read_csv(path + '/velib_stations.csv', sep=',')

data_velib_avec_UIC = pd.merge(data_velib, referentiel_velib, left_on='station_code',
                               right_on="Identifian")

data_velib_avec_UIC_select = data_velib_avec_UIC[['last_reported_datetime', 'Nom_de_la_', 'UIC', 'CodeGare', 'latitude', 'longitude',
                                                  'num_bikes_available', 'mechanical_bikes', 'ebikes', 'num_docks_available']]

data_velib_avec_UIC_select['Date'] = pd.to_datetime(
    data_velib_avec_UIC_select['last_reported_datetime'])

data_velib_avec_UIC_select.columns

data_velib_avec_UIC_select['Capacité vélib'] = data_velib_avec_UIC_select[[
    'num_bikes_available', 'num_docks_available']].sum(axis=1)

data_velib_avec_UIC_select.groupby(["UIC", 'Date', 'CodeGare', 'latitude',
                                           'longitude']).sum(['num_bikes_available', 'mechanical_bikes',
                                                              'ebikes', 'num_docks_available', 'Capacité vélib'])

data_velib_avec_UIC_select.to_csv(
    path + '/data_velib_api.csv', index=False, encoding="UTF-8")

data_velib_avec_UIC_select.columns
data_velib_avec_UIC_select[data_velib_avec_UIC_select["UIC"] != 0]
data_velib_avec_UIC_select["UIC"].value_counts()


###############################
#
# Calculer le score pour un trajet
# avec en entrée une gare origine et
#          destination
#
###############################

# ' Fonction pour calculer le score Mélivélo
# '
# ' Input : score_origine, score_destination, score_bord

def score_total(score_origine, score_destination, score_bord):
    if ((score_origine == 1) | (score_destination == 1) | (score_bord == 3)):
        score_final = "rouge"

    elif ((score_origine != 1) & (score_destination != 1) & (score_bord == 1)):
        score_final = "vert"

    else:
        score_final = "orange"

    return score_total

# ' Fonction pour calculer le score Mélivélo
# '
# ' Input : gare_origine (code UIC), gare_destination (code UIC), date_heure (DD/MM/YYYY - HH:MM:SS)
# '         data_gare_accesssibilité
# '         data_train_confort : dataframe


def Calcul_score_trajet(gare_origine, gare_destination,
                        date_heure, sens, ligne, path):

    dico_level_accessibilite = {1: "Non",
                                3: "Oui",
                                4: "Oui",
                                6: "Oui"}

    path = "C:/Users/9606423P/SNCF/Datalab' Mass Transit GrpO365 - Documents/Rayonnement/Datathon/2025/Hackathon_2025"
    gare_origine = "393306"  # Issy Val de Seine
    gare_destination = "393009"  # Versailles Rive Gauche
    sens = "Vers Sud"
    ligne = "C"
    date_heure = "14/11/2025 - 10:10:04"

    type_jour = date_heure.weekday()
    tranche_horaire = date_heure.hour

    date_heure = datetime.strptime(date_heure, '%d/%m/%Y - %H:%M:%S')

    data_accessibilite = pd.read_csv(
        path + "/Donnees_finales/station_with_parking_usage_and_accessibility.csv")

    data_velib = pd.read_csv(
        path + "/Donnees_finales/data_velib_api.csv")

    data_gare = pd.merge(data_accessibilite, data_velib, how="left",
                         left_on="UIC", right_on="UIC")

    data_gare['UIC'] = data_gare['UIC'].astype(int).astype(str)

    data_on_board = pd.read_csv(
        path + "/Donnees_finales/Scoring_Affluence_velo_juin.csv", sep=";")
    data_on_board["Code_gare"] = data_on_board["Code_gare"].astype(str)

    data_on_board['Date'] = pd.to_datetime(data_on_board['Date'])

    data_on_board['Type_jour'] = data_on_board['Date'].apply(
        lambda x: x.weekday())

    # Selection du perimetre
    data_gare_origine = data_gare[data_gare['UIC'] == gare_origine]
    data_gare_destination = data_gare[data_gare['UIC'] == gare_destination]

    # Il faudrait selectionner le sens
    data_on_board_select = data_on_board[((data_on_board['Par_tranche_horaire'] == tranche_horaire) &
                                         (data_on_board['Type_jour'] == type_jour) &
                                         (data_on_board['Ligne'] == ligne))]

    rg_destination = data_on_board_select['rang'][data_on_board_select["Code_gare"]
                                                  == gare_destination]
    rg_origine = data_on_board_select['rang'][data_on_board_select["Code_gare"] == gare_origine]

    rg_destination = max(rg_destination)
    rg_origine = min(rg_origine)

    data_on_board_select[((data_on_board_select['rang'] > rg_origine) &
                         (data_on_board_select['rang'] < rg_destination))]

    score_bord = max(data_on_board_select['Score'])
    score_origine = min(data_gare_origine['accessibility_level_id'])
    score_destination = min(data_gare_destination['accessibility_level_id'])

    score = score_total(score_origine=score_origine,
                        score_destination=score_destination,
                        score_bord=score_bord)

    nombre_de_places_disponibles_parking_origine = data_gare_origine['num_docks_available_x'].unique()[
        0]
    nombre_de_places_disponibles_velib_origine = max(
        data_gare_origine['num_docks_available_y'].unique())
    accessibilite_en_gare_origine = data_gare_origine['accessibility_level_id'].map(
        dico_level_accessibilite).unique()[0]

    nombre_de_velos_disponibles_destination = data_gare_destination['num_bikes_available'].unique()[
        0]
    accessibilite_en_gare_destination = data_gare_destination['accessibility_level_id'].map(
        dico_level_accessibilite).unique()[0]

    results = pd.DataFrame({'Mélivélo - score': score,
                            gare_origine + " - nombre des places vélos - Parking": nombre_de_places_disponibles_parking_origine,
                            "Gare origine - nombre des places vélos - Vélib": nombre_de_places_disponibles_velib_origine,
                            "Gare origine - accessibilité": accessibilite_en_gare_origine,
                            "Gare destination - nombre de vélos disponibles - Vélib": nombre_de_velos_disponibles_destination,
                            "Gare destination - accessibilité": accessibilite_en_gare_destination}, index=[0])

    results.T
    return (results.T)


Main
Calcul_score_trajet()
