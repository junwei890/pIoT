import os
import sys
import asyncio

from dotenv import load_dotenv
from fastapi import FastAPI, Response, status
from influxdb_client_3 import InfluxDBClient3, Point

from models.models import Kitchen_data, Living_room_data, Response_writer

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


# Endpoint that ingests data from the kitchen
@api.post("/kitchen_data", status_code=201)
async def post_kitchen_data(
    kitchen_data: Kitchen_data, response: Response
) -> Response_writer:
    point = (
        Point("data")
        .tag("location", "kitchen")
        .field("in_kitchen", kitchen_data.in_kitchen)
        .field("stove_on", kitchen_data.stove_on)
    )

    try:
        await asyncio.to_thread(client.write, database=database, record=point)
    except Exception as e:
        fail_msg = f"Unsuccessful write of kitchen data to InfluxDB: {e}"
        print(fail_msg)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return Response_writer(message=fail_msg)

    success_msg = "Successful write of kitchen data to InfluxDB"
    print(success_msg)
    return Response_writer(message=success_msg)


# Endpoint that ingests data from the living room environment
@api.post("/living_room_data", status_code=201)
async def post_living_room_data(
    living_room_data: Living_room_data, response: Response
) -> Response_writer:
    point = (
        Point("data")
        .tag("location", "living room")
        .field("temperature", living_room_data.temperature)
        .field("humidity", living_room_data.humidity)
        .field("illumination", living_room_data.illumination)
    )

    try:
        await asyncio.to_thread(client.write, database=database, record=point)
    except Exception as e:
        fail_msg = f"Unsuccessful write of living room data to InfluxDB: {e}"
        print(fail_msg)
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return Response_writer(message=fail_msg)

    success_msg = "Successful write of living room data to InfluxDB"
    print(success_msg)
    return Response_writer(message=success_msg)
