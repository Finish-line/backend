from sqlmodel import Field, SQLModel

class Driver(SQLModel, table=True):
    id: int = Field(primary_key=True)
    active: bool = Field(default=True)
    car_type: str = Field(nullable=False)
    
    email: str = Field(nullable=False)

    position_lat: float = Field(default=0.)
    position_long: float = Field(default=0.)

class Trip(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)

    driver_accept: bool = Field()

    price: float = Field()
    address: str = Field()

    duration: float = Field()
    distance: float = Field()
    duration_till_pickup: float = Field()
    distance_till_pickup: float = Field()

    start_lat: float = Field()
    start_long: float = Field()
    destination_lat: float = Field()
    destination_long: float = Field()
