######################################
#
#          Main - Mélivélo
#
######################################

import requests
import pandas as pd
import numpy as np
import geopandas as gpd
import requests
import json
import csv
from datetime import datetime
from simpledbf import Dbf5

# parametres
API_BASE = "https://prim.iledefrance-mobilites.fr/marketplace/"
API_KEY = "Zp2fHVIvEVIpWwk2V179vsGHBJbQSh93"  # remplacer par votre clé
HEADERS = {"Accept": "application/json", "apikey": API_KEY}
path = "C:/Users/9606423P/SNCF/Datalab' Mass Transit GrpO365 - Documents/Rayonnement/Datathon/2025/Hackathon_2025"

station_name_to_lat_lon = pd.read_csv(
    path + "/Donnees_finales/station_with_parking_usage_and_accessibility.csv")
station_name_to_lat_lon = (
    station_name_to_lat_lon[["name", "lat", "lon"]
                            ].drop_duplicates().set_index("name")
)

# Date/heure pour le trajet (format : YYYYMMDDTHHMMSS)
TRIP_DATETIME = "20251114T170000"
TRIP_DATETIME = datetime.strptime(TRIP_DATETIME, "%Y%m%dT%H%M%S")

dico_level_accessibilite = {1: "Non",
                            3: "Oui",
                            4: "Oui",
                            6: "Oui"}

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

    return score_final

# ' Fonction pour calculer le score Mélivélo
# '
# ' Input : gare_origine (code UIC), gare_destination (code UIC), date_heure (DD/MM/YYYY - HH:MM:SS)
# '         data_gare_accesssibilité
# '         data_train_confort : dataframe


def calcul_score_trajet(gare_origine, gare_destination, date_heure, ligne, path):

    # gare_origine = "393306"  # Issy Val de Seine
    # gare_destination = "393009"  # Versailles Rive Gauche
    # sens = "Vers Sud"
    # ligne = "C"
    # date_heure = "14/11/2025 - 10:10:04"

    gare_origine = str(gare_origine)
    gare_destination = str(gare_destination)

    type_jour = date_heure.weekday()
    tranche_horaire = date_heure.hour

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
                            "Gare origine - nombre des places vélos - Parking": nombre_de_places_disponibles_parking_origine,
                            "Gare origine - nombre des places vélos - Vélib": nombre_de_places_disponibles_velib_origine,
                            "Gare origine - accessibilité": accessibilite_en_gare_origine,
                            "Gare destination - nombre de vélos Vélib": nombre_de_velos_disponibles_destination,
                            "Gare destination - accessibilité": accessibilite_en_gare_destination}, index=[0])

    print(results.T)

    return (results.T)


def extract_idfm_stop_ids_and_lines(navitia_response: dict):
    """
    Retourne :
      - une liste des stop_ids de type 'stop_point:IDFM:*'
        (montée puis descente pour chaque section 'public_transport'
        de l'itinéraire 'best')
      - une liste des lignes empruntées avec leur direction
        (mode, réseau, label de ligne, direction)
    """
    journeys = navitia_response.get("journeys", [])
    if not journeys:
        return [], []

    # Récupération du meilleur itinéraire
    best_journey = next((j for j in journeys if j.get("type") == "best"), None)
    if best_journey is None:
        best_journey = journeys[0]

    idfm_stop_ids = []
    lines_info = []

    for section in best_journey.get("sections", []):
        if section.get("type") != "public_transport":
            continue

        stops = section.get("stop_date_times", [])
        if not stops:
            continue

        # 1) Récupération des stop_ids IDFM
        idfm_stops = [
            s["stop_point"]["id"]
            for s in stops
            if s["stop_point"]["id"].startswith("stop_point:IDFM:")
        ]

        if idfm_stops:
            # Montée = premier, Descente = dernier
            idfm_stop_ids.append(idfm_stops[0])
            idfm_stop_ids.append(idfm_stops[-1])

        # 2) Récupération des infos de ligne / direction
        display = section.get("display_informations", {})
        lines_info.append({
            "mode": display.get("commercial_mode"),
            "network": display.get("network"),
            "line_label": display.get("label"),
            "direction": display.get("direction"),
        })

    # print("Stop IDs IDFM :", idfm_stop_ids)
    print("Lignes empruntées :")
    for l in lines_info:
        print(f"- {l['mode']} {l['line_label']
                               } ({l['network']}) → {l['direction']}")

    return idfm_stop_ids, lines_info


def get_stations_on_itineraries(origin, destination):

    API_URL = API_BASE + "v2/navitia/journeys"
    # Coordonnées (lon, lat) — des chaînes conviennent pour le tutoriel
    ORIGIN_LON = station_name_to_lat_lon.loc[origin]["lon"]
    ORIGIN_LAT = station_name_to_lat_lon.loc[origin]["lat"]
    DEST_LON = station_name_to_lat_lon.loc[destination]["lon"]
    DEST_LAT = station_name_to_lat_lon.loc[destination]["lat"]

    # Construire l'URL (Navitia attend lon;lat encodé en lon%3B%20lat)
    FROM_PARAM = f"{ORIGIN_LON}%3B{ORIGIN_LAT}"
    TO_PARAM = f"{DEST_LON}%3B{DEST_LAT}"
    URL = f"{API_URL}?from={FROM_PARAM}&to={TO_PARAM}&datetime={TRIP_DATETIME}"

    # Afficher l'URL pour que le lecteur voie comment elle est construite
    # print("Aperçu de l'URL Navitia :")
    # print(URL)

    # APPEL A API NAVITIA

    # Exécuter la requête inline (style tutoriel simple)
    try:
        resp = requests.get(URL, headers=HEADERS)
        # print("Statut HTTP :", resp.status_code)

        if resp.status_code == 200:
            data = resp.json()
            # Aplatir le JSON de premier niveau pour inspection
            df = pd.json_normalize(data)
            # print("Clés de premier niveau :", list(data.keys()))

        else:
            print("Réponse non-200, corps (400 premiers caractères) :")
            print(resp.text[:400])

    except Exception as e:
        print("La requête a échoué :", e)

    # STOPs ET LINES PARCOURUS

    stops, lines = extract_idfm_stop_ids_and_lines(data)

    manual_map_idfm_to_uic = {
        'stop_point:IDFM:monomodalStopPlace:462357': 393306,  # issy val de seine
        'stop_point:IDFM:monomodalStopPlace:43220': 393009,  # versailles chateau
    }

    return [manual_map_idfm_to_uic[stop] for stop in stops], lines


############# MAIN #################

print('')
print('PRE-PROCESSING - affluence vélos')
print('PRE-PROCESSING - accessibilités')
print('PRE-PROCESSING - parking vélos')
print('PRE-PROCESSING - Vélib')

station_origine = 'ISSY-VAL-DE-SEINE'
station_destination = 'VERSAILLES RIVE GAUCHE'

print('')

stop, line = get_stations_on_itineraries(station_origine, station_destination)

print('')

results = calcul_score_trajet(gare_origine=stop[0], gare_destination=stop[1],
                              date_heure=TRIP_DATETIME, ligne=line[0]['line_label'],
                              path=path)
