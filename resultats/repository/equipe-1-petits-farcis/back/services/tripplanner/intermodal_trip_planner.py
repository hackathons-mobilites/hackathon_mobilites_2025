import requests
import geopy.distance
from services.external_services.navitia_pt import calculate_journeys_navitia, transform_journeys_navitia
from services.external_services.graphhopper_car import calculate_journeys_grapphopper, transform_journeys_graphhopper
from services.external_services.geovelo import calculate_journeys_geovelo, transform_journeys_geovelo

BIKEPARK_CSV_PATH = "data/stationnement_velo_en_ile_de_france.csv"
CARPARK_CSV_PATH = "data/parking_relais_idf.csv"

bike_parks = []
car_parks = []


def load_bike_parking_data():
    """
    Load bike parking data from the external source and save it locally.
    
    BikePark
        A list of bike parks {
            "id": str,
            "lat": float,
            "lon": float
        }
    """
    download_bike_parking_data();
    

    with open(BIKEPARK_CSV_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines[1:]:
            parts = line.strip().split(";")
            if len(parts) < 2:
                continue
            geo_point = parts[0]
            lon_lat = geo_point.split(", ")
            if len(lon_lat) != 2:
                continue
            lat = float(lon_lat[0])
            lon = float(lon_lat[1])
            bike_park = {
                "id": parts[2],
                "lat": lat,
                "lon": lon
            }
            bike_parks.append(bike_park)
    print(f"Loaded {len(bike_parks)} bike parking locations.")

def load_car_parking_data():
    """
    Load car parking data from the external source and save it locally.
    
    CarPark
        A list of car parks {
            "id": str,
            "lat": float,
            "lon": float
        }
    """
    download_car_parking_data();
    

    with open(CARPARK_CSV_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines[1:]:
            parts = line.strip().split(";")
            if len(parts) < 2:
                continue
            geo_point = parts[0]
            lon_lat = geo_point.split(", ")
            if len(lon_lat) != 2:
                continue
            lat = float(lon_lat[0])
            lon = float(lon_lat[1])
            car_park = {
                "id": parts[2],
                "lat": lat,
                "lon": lon
            }
            car_parks.append(car_park)
    print(f"Loaded {len(car_parks)} car parking locations.")

def near_parks(parks, lat, lon, min_distance=2000, max_distance=5000):
    """Find bike parks within a certain distance from a given location.
    
    Args:
        parks: List of bike parks
        lat: Latitude of the location
        lon: Longitude of the location
        min_distance: Minimum distance in meters
        max_distance: Maximum distance in meters

    Returns:
        A list of bike parks within the specified distance range
    """
    nearby_parks = []
    for park in parks:
        park_coords = (park["lat"], park["lon"])
        location_coords = (lat, lon)
        distance = geopy.distance.great_circle(park_coords, location_coords).meters
        if min_distance <= distance <= max_distance:
            nearby_parks.append(park)
    return nearby_parks



def download_bike_parking_data():
    """Download bike parking data from the external source."""
    url = "https://data.iledefrance-mobilites.fr/api/explore/v2.1/catalog/datasets/stationnement-velo-en-ile-de-france/exports/csv?lang=fr&timezone=Europe%2FBerlin&use_labels=true&delimiter=%3B"
    response = requests.get(url)
    if response.status_code == 200:
        with open(BIKEPARK_CSV_PATH, "wb") as f:
            f.write(response.content)
        print("Bike parking data downloaded successfully.")
    else:
        print("Failed to download bike parking data.")
 
def download_car_parking_data():
    """Download car parking data from the external source."""
    url = "https://data.iledefrance-mobilites.fr/api/explore/v2.1/catalog/datasets/parking_relais_idf/exports/csv?lang=fr&timezone=Europe%2FBerlin&use_labels=true&delimiter=%3B"
    response = requests.get(url)
    if response.status_code == 200:
        with open(CARPARK_CSV_PATH, "wb") as f:
            f.write(response.content)
        print("Car parking data downloaded successfully.")
    else:
        print("Failed to download car parking data.")



def calculate_journeys_intermodal(from_location, to_location, datetime, park_type="BIKE"):
    """
    Calculate intermodal journeys using bike parking data.
    
    Args:
        from_location: A dictionary with 'lon' and 'lat' for the starting point
        to_location: A dictionary with 'lon' and 'lat' for the destination point
        datetime: A string representing the date and time for the journey
        park_type: Type of parking to consider (default is "BIKE")
        
    Returns:
        A list of intermodal journey options
    """
    # This is a placeholder function. The actual implementation would involve
    # integrating bike parking data into the journey planning process.
    

    distance_to_from = geopy.distance.great_circle(
        (from_location["lat"], from_location["lon"]),
        (to_location["lat"], to_location["lon"])
    ).meters

    min_distance = 2000
    max_distance = distance_to_from / 2

    if park_type == "CAR":
        min_distance = 5000
        max_distance = (distance_to_from / 3)* 2

    if max_distance < min_distance:
        return []

    if park_type == "BIKE":
        nearby_parks = near_parks(bike_parks, from_location["lat"], from_location["lon"], min_distance, max_distance)
    elif park_type == "CAR":
        nearby_parks = near_parks(car_parks, from_location["lat"], from_location["lon"], min_distance, max_distance)
    else:
        return []
    
    print(f"Found {len(nearby_parks)} nearby {park_type} parks for intermodal journey.")
    
    nearest_park = find_nearest_by_park(nearby_parks, to_location)
    if not nearest_park:
        return []
    
    if park_type == "BIKE":
        geovelo_response = calculate_journeys_geovelo(from_location, nearest_park, datetime)
        geovelo_journeys = transform_journeys_geovelo(geovelo_response)

        if(geovelo_journeys is None or len(geovelo_journeys) == 0):
            return []

        first_leg = geovelo_journeys[0]
        date_pt = first_leg["arrival"]

        navitia_response = calculate_journeys_navitia(nearest_park, to_location, date_pt)
        
        navitia_journeys = transform_journeys_navitia(navitia_response)
        if(navitia_journeys is None or len(navitia_journeys) == 0):
            return []
        
        second_leg = navitia_journeys[0]
    else:
        gh_response = calculate_journeys_grapphopper(from_location, nearest_park, datetime)
        gh_journeys = transform_journeys_graphhopper(gh_response)

        if(gh_journeys is None or len(gh_journeys) == 0):
            return []
        
        first_leg = gh_journeys[0]
        date_pt = first_leg["arrival"]

        navitia_response = calculate_journeys_navitia(nearest_park, to_location, date_pt)
        navitia_journeys = transform_journeys_navitia(navitia_response)
        if(navitia_journeys is None or len(navitia_journeys) == 0):
            return []

        second_leg = navitia_journeys[0]


    journey = {}

    departure_time = first_leg["departure"]
    arrival_time = second_leg["arrival"]

    journey["departure"] = departure_time
    journey["arrival"] = arrival_time

    journey["paths"] = first_leg["paths"] + second_leg["paths"]

        
    return [journey]


def find_nearest_by_park(park_list, destination_location):
    """
    Find the nearest park from a list to the destination location.
    
    Args:
        park_list: List of parks with 'lat' and 'lon'
        destination_location: A dictionary with 'lon' and 'lat' for the destination point
    Returns:
        The nearest park dictionary
    """
    nearest_park = None
    min_distance = float('inf')
    for park in park_list:
        park_coords = (park["lat"], park["lon"])
        dest_coords = (destination_location["lat"], destination_location["lon"])
        distance = geopy.distance.great_circle(park_coords, dest_coords).meters
        if distance < min_distance:
            min_distance = distance
            nearest_park = park
    return nearest_park


if __name__ == "__main__":
    load_bike_parking_data()
    load_car_parking_data()

    # print(f"Total bike parks loaded: {len(bike_parks)}")

    # #print the 5 first bike parks
    # for bike_park in bike_parks[:5]:
    #     print(bike_park)

    # # Test near_parks function
    # test_lat = 48.8566  # Paris latitude
    # test_lon = 2.3522   # Paris longitude
    # nearby = near_parks(bike_parks, test_lat, test_lon)
    # print(f"Found {len(nearby)} bike parks near Paris within 2-5 km.")

    legs = calculate_journeys_intermodal(
        from_location={"lon": "2.33792", "lat": "48.55827"},
        to_location={"lon": "2.3588523", "lat": "48.9271087"},
        datetime="20251121T073000",
        park_type="CAR"
    )

    import json

    json.dump(legs, open("intermodal_journeys.json", "w"), indent=2)
    print(f"Found {len(legs)} intermodal journeys.")
    if len(legs) > 0:
     
        print(json.dumps(legs[0], indent=2))