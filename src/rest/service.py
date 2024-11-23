from geopy.distance import geodesic

import googlemaps

from src.config import GOOGLE_MAPS_API_KEY

gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)

def calculate_box(lat, long, radius):
    center = (lat, long)
    north = geodesic(kilometers=radius).destination(center, 0)
    south = geodesic(kilometers=radius).destination(center, 180)
    east = geodesic(kilometers=radius).destination(center, 90)
    west = geodesic(kilometers=radius).destination(center, 270)
    
    return north, south, east, west

def calculate_time_distance(
    origin_lat,
    origin_long,
    destination_lat,
    destination_long
):
    origin = str(origin_lat) + ", " + str(origin_long)
    destination = str(destination_lat) + ", " + str(destination_long)
    
    distance_matrix = gmaps.distance_matrix(origin, destination, mode="driving")
    
    duration = distance_matrix['rows'][0]['elements'][0]['duration']['value'] / 60
    distance = distance_matrix['rows'][0]['elements'][0]['distance']['value'] / 1000
    return duration, distance

