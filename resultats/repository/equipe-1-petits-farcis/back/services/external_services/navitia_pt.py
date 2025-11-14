import os
import requests
from dotenv import load_dotenv
import geopy.distance
load_dotenv()


API_BASE = "https://prim.iledefrance-mobilites.fr/marketplace/"
NAVITIA_API_KEY = os.environ.get("NAVITIA_API_KEY")
API_URL = API_BASE + "v2/navitia/journeys"


def calculate_journeys_navitia(from_location, to_location, datetime):
    """
    Calculate journeys between two locations using the external API.

    Args:
        from_location: A dictionary with 'lon' and 'lat' for the starting point
        to_location: A dictionary with 'lon' and 'lat' for the destination point
        datetime: A string representing the date and time for the journey
    Returns:
        The JSON response from the API containing journey options
    """

    headers = {"Accept": "application/json", "apikey": NAVITIA_API_KEY}
    from_param = f"{from_location['lon']}%3B{from_location['lat']}"
    to_param  = f"{to_location['lon']}%3B{to_location['lat']}"
    url = f"{API_URL}?from={from_param}&to={to_param}&datetime={datetime}"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print("Error fetching journeys:", e)
        return None


def transform_journey_navitia(journey):
    """
    Transform a journey from the API response into a simplified format.
    
    Args:
        journey: A journey object from the API response
        
    Returns:
        A dictionary with simplified journey information
    """
    result = {
        "departure": journey.get("departure_date_time"),
        "arrival": journey.get("arrival_date_time"),
        "paths": []
    }
    
    for section in journey.get("sections", []):
        # Only include public transport and street network sections
        if section.get("type") in ["public_transport", "street_network"]:
            # Get coordinates and convert to encoded polyline
            coordinates = section.get("geojson", {}).get("coordinates", [])
            # Convert from [lon, lat] to (lat, lon) format for polyline encoding
            coords_for_polyline = [(lat, lon) for lon, lat in coordinates]
         
            # Get CO2 emission data
            co2_data = section.get("co2_emission", {})
            co2_value = co2_data.get("value", 0)
            
            path = {
                "mode": section.get("mode") or section.get("type"),
                "shape": coords_for_polyline,
                "line": None,
                "departure": section.get("departure_date_time"),
                "arrival": section.get("arrival_date_time"),
                "color": None,
                "co2": co2_value
            }
            
            # Add line and color info for public transport
            if section.get("type") == "public_transport":
                display_info = section.get("display_informations", {})
                path["line"] = display_info.get("code")
                path["color"] = display_info.get("color")
                path["mode"] = display_info.get("commercial_mode")
            
            result["paths"].append(path)


    #Filter out journeys that are only walking over long distances
    if len(result["paths"]) == 1 and result["paths"][0]["mode"] == "walking" and len(journey.get("sections", [])) == 1:    
        distances = journey.get("distances")
        if distances:
            walking_distance = distances.get("total", 0)
            if walking_distance is None or walking_distance == 0:
                walking_distance = distances.get("walking", 0)
            if walking_distance > 1000:
                return None
    
    return result


def transform_journeys_navitia(journeys_response):
    """
    Transform multiple journeys from the API response.
    
    Args:
        journeys_response: The full API response containing journeys
        
    Returns:
        A list of simplified journey objects
    """

    journey_list = []
    for journey in journeys_response.get("journeys", []):
        transformed = transform_journey_navitia(journey)
        if transformed:
            journey_list.append(transformed)
    return journey_list