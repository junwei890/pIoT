from pydantic import BaseModel


class Kitchen_data(BaseModel):
    in_kitchen: bool
    stove_on: bool


class Living_room_data(BaseModel):
    temperature: float
    humidity: float
    illumination: int


class Response_writer(BaseModel):
    message: str
