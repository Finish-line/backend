import fastapi

from fastapi import HTTPException, status
from sqlmodel import select

from src.rest.service import calculate_time_distance

router = fastapi.APIRouter(prefix="/api")

@router.get("/distance")
def calculate_distance(
    start_lat: float,
    start_long: float,
    dest_lat: float,
    dest_long: float):
    duration, distance = calculate_time_distance(start_lat, start_long, dest_lat, dest_long)
    
    return {'duration':duration, 'distance':distance}
    

rides = [
    {'id': 0, 'price': 0.05, 'duration' : 600, 'start': 'Schwabing-West', 'start_lat': 48.165980,'start_long': 11.556090, 'destination': 'Schwabing-Freimann', 'destination_lat': 48.188645, 'destination_long':11.585273},
    {'id': 1, 'price': 0.08, 'duration' : 1560, 'start': 'Schwabing-West', 'start_lat': 48.157868,'start_long': 11.561289, 'destination': 'Bogenhausen', 'destination_lat': 48.146300, 'destination_long':11.606730},
    {'id': 2, 'price': 0.06, 'duration' : 720, 'start': 'Schwabing-West', 'start_lat': 48.160261,'start_long': 11.551723, 'destination': 'Neuhausen-Nymphenburg', 'destination_lat': 48.148188, 'destination_long':11.508284},
    {'id': 3, 'price': 0.04, 'duration' : 960, 'start': 'Altstadt-Lehel', 'start_lat': 48.137020,'start_long': 11.580554, 'destination': 'Feldmüllerweg', 'destination_lat': 48.113244, 'destination_long':11.585446},
    {'id': 4, 'price': 0.03, 'duration' : 540, 'start': 'Altstadt-Lehel', 'start_lat': 48.138376,'start_long': 11.580843, 'destination': 'Sendling', 'destination_lat': 48.118267, 'destination_long':11.552381}
]

@router.get("/rides")
def get_trips():
    return rides
