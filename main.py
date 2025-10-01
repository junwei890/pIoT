from fastapi import FastAPI
from influxdb_client_3 import InfluxDBClient3
import os

# Initialising a database client
token = os.environ.get("DB_TOKEN")
host = os.environ.get("DB_URL")
if token is None or host is None:
    print("database token or host not set in environment variables")
    os.exit(1)

org = "IOT"
client = InfluxDBClient3(host=host, token=token, org=org)

# Initialising FastAPI
api = FastAPI()


@api.get("/")
async def root():
    return {"message": "Hello World!"}
