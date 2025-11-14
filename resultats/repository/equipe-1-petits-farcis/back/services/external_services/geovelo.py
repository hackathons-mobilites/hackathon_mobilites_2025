import os
import requests
from dotenv import load_dotenv
import polyline

load_dotenv()

GEOVELO_API_KEY = os.environ.get("GEOVELO_API_KEY")
GEOVELO_URL = "https://prim.iledefrance-mobilites.fr/marketplace/computedroutes?instructions=false&elevations=false&geometry=true&single_result=true&bike_stations=true&objects_as_ids=true&merge_instructions=false&show_pushing_bike_instructions=false"


def calculate_journeys_geovelo(from_location, to_location, datetime):

    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "apikey": GEOVELO_API_KEY
    }

    payload = {
        "waypoints": [
            {
                "latitude": from_location['lat'],
                "longitude": from_location['lon']
            },
            {
                "latitude": to_location['lat'],
                "longitude": to_location['lon']
            }
        ],
        "datetimeOfDeparture": datetime,
        "transportModes": [
            "BIKE"
        ]
    }

    url = GEOVELO_URL
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print("Error fetching journeys from Geovelo:", e)
        return None
    

def transform_journeys_geovelo(geovelo_response):
    """
    Transform Geovelo API response into the same simplified format as Navitia journeys.
    
    Args:
        geovelo_response: The Geovelo API response (array of route objects)
        
    Returns:
        A list of simplified journey objects compatible with Navitia format
    """
    journey_list = []

    # geovelo_response is an array of route objects
    for route in geovelo_response[:1]:
        # Get departure and arrival times from the route level
        departure_time = route.get("estimatedDatetimeOfDeparture", "")
        arrival_time = route.get("estimatedDatetimeOfArrival", "")
        
        # Convert ISO format to the format used by Navitia (YYYYMMDDTHHmmss)
        if departure_time:
            departure_time = departure_time.replace("-", "").replace(":", "").replace(" ", "T")
        if arrival_time:
            arrival_time = arrival_time.replace("-", "").replace(":", "").replace(" ", "T")
        
        journey = {
            "departure": departure_time,
            "arrival": arrival_time,
            "paths": []
        }

        # Process each section in the route
        for section in route.get("sections", []):
            # Get section times
            section_departure = section.get("estimatedDatetimeOfDeparture", "")
            section_arrival = section.get("estimatedDatetimeOfArrival", "")
            
            # Convert ISO format
            if section_departure:
                section_departure = section_departure.replace("-", "").replace(":", "").replace(" ", "T")
            if section_arrival:
                section_arrival = section_arrival.replace("-", "").replace(":", "").replace(" ", "T")
            
            # Get geometry and decode it from encoded polyline format
            geometry_encoded = section.get("geometry", "")
            if geometry_encoded:
                # Decode the polyline to get list of (lat, lon) tuples
                coords_for_polyline = polyline.decode(geometry_encoded,6)
            else:
                # Fallback to waypoints if geometry is not available
                waypoints = section.get("waypoints", [])
                coords_for_polyline = [(float(wp["latitude"]), float(wp["longitude"])) for wp in waypoints]
            
            # Get details
            details = section.get("details", {})
            distances = details.get("distances", {})
            total_distance = distances.get("total", 0)
            
            # CO2 for bike is 0
            path = {
                "mode": section.get("transportMode", "BIKE").lower(),
                "shape": coords_for_polyline,
                "line": None,
                "departure": section_departure,
                "arrival": section_arrival,
                "color": None,
                "co2": 0  # Bike has zero CO2 emissions
            }
            journey["paths"].append(path)

        journey_list.append(journey)

    return journey_list

if __name__ == "__main__":
    from_location = {"lon": "2.33792", "lat": "48.85827"}
    to_location = {"lon": "2.3588523", "lat": "48.9271087"}
    date_time = "20251121T073000"

    response = calculate_journeys_geovelo(from_location, to_location, date_time)

    #save response to a file
    with open("geovelo_response.json", "w") as f:
        import json
        json.dump(response, f)

    if response:
        journeys = transform_journeys_geovelo(response)
        import json
        print(f"Found {len(journeys)} journeys from Geovelo")
        print(json.dumps(journeys[0], indent=2))