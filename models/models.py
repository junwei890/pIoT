from pydantic import BaseModel


class kitchen_data(BaseModel):
    in_kitchen: bool
    stove_on: bool


class kitchen_data_2(BaseModel):
    air_purity: float
    volatile_concentration: float


class living_room_data(BaseModel):
    temperature: float
    humidity: float
    illumination: int


class response_writer(BaseModel):
    message: str
