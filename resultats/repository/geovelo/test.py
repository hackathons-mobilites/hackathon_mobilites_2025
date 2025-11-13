import sys
import argparse
import json
import requests
import polyline
from shapely.geometry import LineString

# author : esgn

def parse_args():
    parser = argparse.ArgumentParser("Script description")
    parser.add_argument("--lon_start",
                        help="lon start",
                        default="2.33261")
    parser.add_argument("--lat_start",
                        help="lat start",
                        default="48.862096")
    parser.add_argument("--lon_end",
                        help="lon end",
                        default="2.32134")
    parser.add_argument("--lat_end",
                        help="lat end",
                        default="48.83059")
    parser.add_argument("--instructions",
                        help="instructions",
                        action="store_true")
    parser.add_argument("--elevations",
                        help="elevations",
                        action="store_true")
    parser.add_argument("--geometry",
                        help="geometry",
                        action="store_true")
    parser.add_argument("--single_result",
                        help="single_result",
                        action="store_true")
    parser.add_argument("--bike_stations",
                        help="bike_stations",
                        action="store_true")
    parser.add_argument("--objects_as_ids",
                        help="objects_as_ids",
                        action="store_true",
                        default=True)
    parser.add_argument("--merge_instructions",
                        help="merge_instructions",
                        action="store_true")
    parser.add_argument("--show_pushing_bike_instructions",
                        help="show_pushing_bike_instructions",
                        action="store_true")     
    return parser.parse_args()


def main():
    API_BASE = "https://prim.iledefrance-mobilites.fr/marketplace/"
    API_KEY = "xxxxxxxxxxxxxxxxxxxxxxxx"  # remplacer par votre clé
    HEADERS = {"Accept": "application/json", "Content-Type": "application/json", "apikey": API_KEY}
    args = parse_args()

    # Construction du payload
    # Seul waypoints est obligatoire. On ajoute les autres paramètres sur la base de l'exemple PRIM.
    json_data={
        "waypoints": [
                    {
                            "latitude": args.lat_start,
                            "longitude": args.lon_start,
                            "title": "Start"
                    },
                    {
                            "latitude": args.lat_end,
                            "longitude": args.lon_end,
                            "title": "End"
                    }
                ],
                "datetimeOfDeparture": "2022-01-31T12:00:00+02:00",
                "datetimeOfArrival": "2022-01-31T12:00:00+02:00",
                "bikeDetails": {
                    "profile": "MEDIAN",
                    "bikeType": "TRADITIONAL",
                    "averageSpeed": 16,
                    "eBike": False,
                    "bikeStations": [
                        {
                            "from": 0,
                            "to": 0
                        }
                    ]
                },
                "transportModes": [
                    "BIKE"
                ]
    }

    # URL de l'API avec paramètres optionnels
    url = ( f"https://prim.iledefrance-mobilites.fr/marketplace/computedroutes?"
           f"instructions={args.instructions}"
           f"&elevations={args.elevations}"
           f"&geometry={args.geometry}"
           f"&single_result={args.single_result}"
           f"&bike_stations={args.bike_stations}"
           f"&objects_as_ids={args.objects_as_ids}"
           f"&merge_instructions={args.merge_instructions}"
           f"&show_pushing_bike_instructions={args.show_pushing_bike_instructions}" )
    
    resp = requests.post(url, headers=HEADERS, json=json_data)

    if(resp.status_code==200):

        json_resp = resp.json()
        # json_dump = json.dumps(json_resp, indent=4)
        # print("Response JSON:\n", json_dump)
        
        # On suppose qu'on a qu'une seule section dans la réponse
        geometry = json_resp[0]['sections'][0]['geometry']
        distance = json_resp[0]['distances']['total']
        duration = json_resp[0]['duration']

        # Précision non standard de 6 décimales pour geovelo. Polyline par défaut à 5.
        decoded_polyline = polyline.decode(geometry, precision=6)
        coords_lonlat = [(lon, lat) for (lat, lon) in decoded_polyline]
        line = LineString(coords_lonlat)

        # Impression des résultats
        print(distance)
        print(duration)
        print(line.wkt)

if __name__ == '__main__':
    sys.exit(main())
