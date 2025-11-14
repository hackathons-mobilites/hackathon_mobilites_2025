import requests
import os
import math
from services.external_services.geovelo import calculate_journeys_geovelo, transform_journeys_geovelo
import polyline
from services.external_services.graphhopper_car import calculate_journeys_grapphopper, transform_journeys_graphhopper
from services.external_services.navitia_pt import calculate_journeys_navitia, transform_journeys_navitia
from services.tripplanner.intermodal_trip_planner import calculate_journeys_intermodal
import geopy.distance

def add_gifts_to_journeys(journey, number_of_gifts):
    """
    Add a number of gifts to the journey.
    The gifts are dispatched regularly on the different paths of the journey.
    The coordinates are used to find the intervals for gift distribution.
    Add fields "gifts" to the journey. 
    "  "gifts": [
    { "id": "gift_1", "lat": 48.8612, "lon": 2.3421 },
    { "id": "gift_2", "lat": 48.8673, "lon": 2.3517 }
  ]
    
    Args:
        journey: A simplified journey object
        number_of_gifts: The number of gifts to distribute based on CO2 savings

    Returns:
        The updated journey object with gift information added
    """
    
    total_paths = len(journey["paths"])
    if total_paths == 0:
        return journey

    all_coordinates = []

    total_distance = 0.0

    for path in journey["paths"]:
        all_coordinates.extend(path["shape"])
        total_distance += geopy.distance.great_circle(path["shape"][0], path["shape"][-1]).meters


    interval_distance = total_distance / (number_of_gifts + 1)

    total_coordinates = len(all_coordinates)
    
    current_distance = 0.0
    gifts = []
    for i in range(0, total_coordinates-2):
        
        current_distance += geopy.distance.great_circle(all_coordinates[i], all_coordinates[i+1]).meters

        if current_distance > interval_distance:
            gift_id = len(gifts) + 1
            lat, lon = all_coordinates[i+1]
            gifts.append({
                "id": f"gift_{gift_id}",
                "lat": lat,
                "lon": lon
            })
            current_distance = current_distance - interval_distance
            if len(gifts) >= number_of_gifts:
                break

    journey["gifts"] = gifts
    return journey


def calculate_journeys_with_gifts(from_location, to_location, datetime):
    
    all_journeys = []
    journeys_navitia = calculate_journeys_navitia(from_location, to_location, datetime)
    if journeys_navitia:
        simplified_journeys = transform_journeys_navitia(journeys_navitia)
        for journey in simplified_journeys:
            journey["number_of_gifts"] = 5
        all_journeys.extend(simplified_journeys)


    journey_gh_car = calculate_journeys_grapphopper(from_location, to_location, datetime)
    if journey_gh_car:
        simplified_gh_journeys = transform_journeys_graphhopper(journey_gh_car)
        for journey in simplified_gh_journeys:
            journey["number_of_gifts"] = 1
        all_journeys.extend(simplified_gh_journeys)

    journey_geovelo = calculate_journeys_geovelo(from_location, to_location, datetime)
    if journey_geovelo:
        simplified_geovelo_journeys = transform_journeys_geovelo(journey_geovelo)
        for journey in simplified_geovelo_journeys:
            journey["number_of_gifts"] = 10
        all_journeys.extend(simplified_geovelo_journeys)

    journey_intermodal_bike = calculate_journeys_intermodal(from_location, to_location, datetime, "BIKE")
    if journey_intermodal_bike:
        for journey in journey_intermodal_bike:
            journey["number_of_gifts"] = 7
        all_journeys.extend(journey_intermodal_bike)

    journey_intermodal_car = calculate_journeys_intermodal(from_location, to_location, datetime, "CAR")
    if journey_intermodal_car:
        for journey in journey_intermodal_car:
            journey["number_of_gifts"] = 3
        all_journeys.extend(journey_intermodal_car)

    for journey in all_journeys:
        total_co2 = sum(path["co2"] for path in journey["paths"])
        journey["co2"] = total_co2
    
    for journey in all_journeys:
        journey_with_gifts = add_gifts_to_journeys(journey, journey["number_of_gifts"])

        # encode shape back to polyline for visualization
        for path in journey_with_gifts["paths"]:
            path["shape"] = polyline.encode(path["shape"])


    #sort journeys by co2   
    all_journeys.sort(key=lambda x: x["co2"])

    return all_journeys



if __name__ == "__main__":

    date_time = "20251121T073000"
    from_location = {"lon": "2.33792", "lat": "48.85827"}
    to_location = {"lon": "2.3588523", "lat": "48.9271087"}

    journeys = calculate_journeys_with_gifts(from_location, to_location, date_time)
    if journeys:
        import json
        print(f"Found {len(journeys)} journeys")
        print(json.dumps(journeys[0], indent=2))
    else:
        print("No journeys found")

    # response_gh = calculate_journeys_grapphopper(from_location, to_location, date_time)
    
    # response_simplified = transform_journeys_graphhopper(response_gh)
    # import json
    # print(json.dumps(response_simplified, indent=2))

