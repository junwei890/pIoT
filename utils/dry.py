import asyncio
from influxdb_client_3 import InfluxDBClient3, Point
from fastapi import Response, status


# Function that writes to InfluxDB
async def influxdb3_write(
    location: str,
    database: str,
    point: Point,
    client: InfluxDBClient3,
    response: Response,
) -> str:
    try:
        await asyncio.to_thread(client.write, database=database, record=point)
        msg = f"Successful write of {location} data to InfluxDB"
    except Exception as e:
        msg = f"Unsuccessful write of {location} data to InfluxDB: {e}"
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    print(msg)
    return msg
