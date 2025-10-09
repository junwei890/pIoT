from pydantic import BaseModel

class Kitchen_data(BaseModel):
    in_kitchen: bool
    stove_on: bool

class Response_writer(BaseModel):
    message: str