import os
import sys

from dotenv import load_dotenv
from fastapi import FastAPI, Response
from influxdb_client_3 import InfluxDBClient3, Point

from models.models import (
    kitchen_data,
    kitchen_data_2,
    living_room_data,
    response_writer,
)
from utils.dry import influxdb3_write

# Initialising a database client
load_dotenv()
token = os.environ.get("DB_TOKEN")
host = os.environ.get("DB_URL")
if token is None or host is None:
    print("database token or host not set in environment variables")
    sys.exit(1)

org = "IOT"
client = InfluxDBClient3(host=host, token=token, org=org)
database = "IoT-Data"

# Initialising FastAPI
api = FastAPI()


# Endpoints that ingest data from the kitchen
@api.post("/kitchen_data", status_code=201)
async def post_kitchen_data(
    kitchen_data: kitchen_data, response: Response
) -> response_writer:
    location = "kitchen"
    point = (
        Point(location)
        .field("in_kitchen", kitchen_data.in_kitchen)
        .field("stove_on", kitchen_data.stove_on)
    )

    msg = await influxdb3_write(location, database, point, client, response)
    return response_writer(message=msg)


@api.post("/kitchen_data_2", status_code=201)
async def post_kitchen_data_2(
    kitchen_data_2: kitchen_data_2, response: Response
) -> response_writer:
    location = "kitchen 2"
    point = (
        Point(location)
        .field("air_purity", kitchen_data_2.air_purity)
        .field("volatile_concentration", kitchen_data_2.volatile_concentration)
    )

    msg = await influxdb3_write(location, database, point, client, response)
    return response_writer(message=msg)


# Endpoint that ingests data from the living room
@api.post("/living_room_data", status_code=201)
async def post_living_room_data(
    living_room_data: living_room_data, response: Response
) -> response_writer:
    location = "living room"
    point = (
        Point(location)
        .field("temperature", living_room_data.temperature)
        .field("humidity", living_room_data.humidity)
        .field("illumination", living_room_data.illumination)
    )

    msg = await influxdb3_write(location, database, point, client, response)
    return response_writer(message=msg)
