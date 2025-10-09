import os
import asyncio

from fastapi import FastAPI, Response, status
from influxdb_client_3 import InfluxDBClient3, Point

from models.models import Kitchen_data, Response_writer

# Initialising a database client
token = os.environ.get("DB_TOKEN")
host = os.environ.get("DB_URL")
if token is None or host is None:
    print("database token or host not set in environment variables")
    os.exit(1)

org = "IOT"
client = InfluxDBClient3(host=host, token=token, org=org)
database = "IoT-Data"

# Initialising FastAPI
api = FastAPI()


# Endpoint that ingests data from the kitchen
@api.post("/kitchen_data/", status_code=201)
async def root(kitchen_data: Kitchen_data, response: Response) -> Response_writer:
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
        return Response_writer(message = fail_msg)

    success_msg = "Successful write of kitchen data to InfluxDB"
    print(success_msg)
    return Response_writer(message = success_msg)