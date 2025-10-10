from pydantic import BaseModel


class Kitchen_data(BaseModel):
    in_kitchen: bool
    stove_on: bool


class Kitchen_data_2(BaseModel):
    air_purity: float
    volatile_concentration: float


class Living_room_data(BaseModel):
    temperature: float
    humidity: float
    illumination: int


class Response_writer(BaseModel):
    message: str
