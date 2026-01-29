from pydantic import BaseModel

class HouseInput(BaseModel):
    Square_Footage: float
    Bedrooms: int
    Bathrooms: float
    Age: int
    Garage_Spaces: int
    Lot_Size: float
    Floors: int
    Neighborhood_Rating: float
    Condition: str
    School_Rating: float
    Has_Pool: int
    Renovated: int
    Location_Type: str
    Distance_To_Center_KM: float
