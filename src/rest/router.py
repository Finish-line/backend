import fastapi

from fastapi import HTTPException, status
from sqlmodel import select

from src import models
from src.database import SessionDep
from src.auth.dependencies import TokenDependency
from src.rest.service import calculate_box, calculate_time_distance

router = fastapi.APIRouter(prefix="/api")


@router.get('/search/driver')
def get_drivers_in_area(
    session: SessionDep,
    token: TokenDependency,
    lat: float,
    long: float,
    radius: float
):
    north, east, south, west = calculate_box(lat, long, radius)

    response = session.exec(
        select(models.Driver)
        .where(models.Driver.active == True)
        .where(models.Driver.position_lat >= west)
        .where(models.Driver.position_lat <= east)
        .where(models.Driver.position_long >= north)
        .where(models.Driver.position_long <= south)
    ).all()

    return response


@router.get('/driver/{id}')
def get_driver(
    id:int,
    session: SessionDep,
#    token: TokenDependency
):
    driver_data = session.get(models.Driver, id)

    if driver_data is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND
        )
    
    return driver_data

@router.post('/driver')
@router.put('/driver')
def create_or_update_driver(
    payload: models.Driver,
    session: SessionDep,
    token: TokenDependency
):
    try:
        # Assume `sub` is retrieved from an authenticated token
        email = token.email  # Replace with the appropriate token logic (e.g., token.sub())

        # Query to find existing driver data
        driver = session.exec(
            select(models.Driver)
            .where(models.Driver.email == email)
        ).one_or_none()

        if driver:
            # Update existing driver
            driver_data = payload.model_dump(exclude_unset=True)
            driver.sqlmodel_update(driver_data)

        else:
            # Create new driver
            driver = models.Driver(**payload.model_dump())

        session.add(driver)
        session.commit()
        session.refresh(driver)

        return payload

    except Exception as exc:
        session.rollback()
        print(f"Error occurred: {exc}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST
        )

@router.post("/trip")
def create_trip(
    session: SessionDep,
    token: TokenDependency,
    payload: models.Trip
):
    duration, distance = calculate_time_distance(payload['start_lat'], payload['start_long'], payload['destination_lat'], payload['destination_long'])
    new_trip = models.Trip(
        {
            **payload.model_dump(exclude_unset=True),
            'duration': duration,
            'distance': distance
        }
    )

    try:
        session.add(new_trip)
        session.commit()
        session.refresh(new_trip)
    except Exception as exc:
        session.rollback()
        raise HTTPException(status.HTTP_400_BAD_REQUEST)

    return new_trip


@router.delete("/trip/{id}")
def delete_trip(
    id:int,
    session: SessionDep,
    token: TokenDependency
):
    try:
        trip = session.get(models.Trip, id)

        session.delete(trip)
        session.commit()
    except Exception as exc:
        session.rollback()
        raise HTTPException(status.HTTP_400_BAD_REQUEST)


@router.put("/driver/trip/{id}/accept")
def driver_accept(id: int,
                  session: SessionDep,
                  token: TokenDependency):
    try:
        trip = session.get(models.Trip, id)
        driver = session.exec(
            select(models.Driver)
            .where(models.Driver.email == token.email)
        ).one_or_none()
        
        distance, duration = calculate_time_distance(
            driver.position_lat,
            driver.position_long,
            trip.start_lat,
            trip.start_long
        )
        
        trip.driver_accept = True
        trip.distance_till_pickup = distance
        trip.duration_till_pickup = duration
    
        session.add(trip)
        session.commit()
        session.refresh(trip)
    except Exception as exc:
        session.rollback()
        raise HTTPException(status.HTTP_400_BAD_REQUEST)

    return trip

@router.put("/rider/trip/{id}/accept")
def rider_trip(
    id:int,
    session: SessionDep,
    token: TokenDependency
):
    try:
        trip = session.get(models.Trip, id)
        trip.rider_accept = True
    
        session.add(trip)
        session.commit()
        session.refresh(trip)
    except Exception as exc:
        session.rollback()
        raise HTTPException(status.HTTP_400_BAD_REQUEST)

    return trip
