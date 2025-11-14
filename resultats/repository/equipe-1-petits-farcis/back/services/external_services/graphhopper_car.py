
import os
import requests
from dotenv import load_dotenv

load_dotenv()

GH_API_KEY = os.environ.get("GRAPPHOPPER_API_KEY")


def calculate_journeys_grapphopper(from_location, to_location, datetime):
    """
    Calculate journeys between two locations using the GraphHopper API.

    Args:
        from_location: A dictionary with 'lon' and 'lat' for the starting point
        to_location: A dictionary with 'lon' and 'lat' for the destination point
        datetime: A string representing the date and time for the journey
    Returns:
        The JSON response from the API containing journey options
    """

    headers = {"Accept": "application/json"}
    from_param = f"{from_location['lat']},{from_location['lon']}"
    to_param  = f"{to_location['lat']},{to_location['lon']}"
    url = f"https://graphhopper.com/api/1/route?point={from_param}&point={to_param}&profile=car&locale=fr&calc_points=true&key={GH_API_KEY}&points_encoded=false"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print("Error fetching journeys from GraphHopper:", e)
        return None
    


def transform_journeys_graphhopper(graphhopper_response):
    """
    Transform GraphHopper API response into the same simplified format as Navitia journeys.
    
    Args:
        graphhopper_response: The full GraphHopper API response containing paths
        
    Returns:
        A list of simplified journey objects compatible with Navitia format
    """
    from datetime import datetime, timedelta
    
    journey_list = []
    
    for path in graphhopper_response.get("paths", []):
        # Calculate departure and arrival times
        # GraphHopper doesn't provide absolute times, so we use relative time from now
        now = datetime.now()
        time_seconds = path.get("time", 0) / 1000  # Convert milliseconds to seconds
        departure_time = now.strftime("%Y%m%dT%H%M%S")
        arrival_time = (now + timedelta(seconds=time_seconds)).strftime("%Y%m%dT%H%M%S")
        
        # Get coordinates from the path
        coordinates = path.get("points", {}).get("coordinates", [])
        # Convert from [lon, lat] to (lat, lon) format
        coords_for_polyline = [(lat, lon) for lon, lat in coordinates]
        
        # Calculate CO2 emission for car (approximate: 120g CO2/km for average car)
        distance_km = path.get("distance", 0) / 1000
        co2_value = distance_km * 120  # grams of CO2
        
        # Create a single path for the car journey
        journey_path = {
            "mode": "car",
            "shape": coords_for_polyline,
            "line": None,
            "departure": departure_time,
            "arrival": arrival_time,
            "color": None,
            "co2": co2_value
        }
        
        # Create the journey object
        journey = {
            "departure": departure_time,
            "arrival": arrival_time,
            "paths": [journey_path]
        }
        
        journey_list.append(journey)
    
    return journey_list
