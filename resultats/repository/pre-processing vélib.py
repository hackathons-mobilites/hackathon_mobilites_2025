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
