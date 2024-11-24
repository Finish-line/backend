import fastapi

from fastapi import HTTPException, status

from src.rest.service import calculate_time_distance

router = fastapi.APIRouter(prefix="/api")

@router.get("/distance")
def calculate_distance(
    start_lat: float,
    start_long: float,
    dest_lat: float,
    dest_long: float
):
    try:
        duration, distance = calculate_time_distance(start_lat, start_long, dest_lat, dest_long)
        
        return {'duration':duration, 'distance':distance}
    except Exception as exc:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)

rides = [
    {'id': 0, 'price': 0.05, 'duration' : 600, 'start': 'Schwabing-West', 'startLat': 48.165980,'startLong': 11.556090, 'destination': 'Schwabing-Freimann', 'destLat': 48.188645, 'destLong':11.585273, 'distance':5230},
    {'id': 1, 'price': 0.08, 'duration' : 1560, 'start': 'Schwabing-West', 'startLat': 48.157868,'startLong': 11.561289, 'destination': 'Bogenhausen', 'destLat': 48.146300, 'destLong':11.606730, 'distance':11300},
    {'id': 2, 'price': 0.06, 'duration' : 720, 'start': 'Schwabing-West', 'startLat': 48.160261,'startLong': 11.551723, 'destination': 'Neuhausen-Nymphenburg', 'destLat': 48.148188, 'destLong':11.508284, 'distance':7020},
    {'id': 3, 'price': 0.04, 'duration' : 960, 'start': 'Altstadt-Lehel', 'startLat': 48.137020,'startLong': 11.580554, 'destination': 'Feldmüllerweg', 'destLat': 48.113244, 'destLong':11.585446, 'distance':9800},
    {'id': 4, 'price': 0.03, 'duration' : 540, 'start': 'Altstadt-Lehel', 'startLat': 48.138376,'startLong': 11.580843, 'destination': 'Sendling', 'destLat': 48.118267, 'destLong':11.552381, 'distance':2700}
]


@router.get("/rides")
def get_rides():
    return rides

@router.get("/ride/{id}")
def get_ride(id: int):
    for ride in rides:
        if ride['id'] == id:
            return ride
    
    raise HTTPException(status.HTTP_404_NOT_FOUND)

@router.post("/ride")
def create_ride(
    price:int,
    start:str,
    start_lat:float,
    start_long:float, 
    dest:str,
    dest_lat:float,
    dest_long:float
):
    id = rides[-1]['id'] + 1
    duration, distance = calculate_time_distance(start_lat, start_long, dest_lat, dest_long)
    new_ride = {
        'id' : id,
        'price': price,
        'duration' : duration,
        'start' : start,
        'startLat' : start_lat,
        'startLong': start_long,
        'destination': dest,
        'destLat': dest_lat,
        'destLong' : dest_long,
        'distance': distance
    }
    
    rides.append(new_ride)
    
    return new_ride


@router.put("/rides/claim/{id}")
def claim_ride(id:int):
    ride = rides[id]
    
    rides.remove(ride)
    return ride
