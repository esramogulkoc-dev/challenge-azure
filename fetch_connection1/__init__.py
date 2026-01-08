import logging
import requests
import pymssql
import azure.functions as func
import os

server = os.environ.get("SQL_SERVER")
database = os.environ.get("SQL_DATABASE")
username = os.environ.get("SQL_USERNAME")
password = os.environ.get("SQL_PASSWORD")

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    from_station = req.params.get('from_station') or "Leuven"
    to_station = req.params.get('to_station') or "Gent-Sint-Pieters"

    url = (
        f"https://api.irail.be/connections/"
        f"?from={from_station}&to={to_station}&format=json&alerts=false"
    )

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        connections = data.get('connection', [])

        conn = pymssql.connect(
            server=server,
            user=username,
            password=password,
            database=database
        )
        cursor = conn.cursor()

        for conn_item in connections:
            departure_time = conn_item.get('departure', {}).get('time')
            arrival_time = conn_item.get('arrival', {}).get('time')
            vehicle = conn_item.get('vehicle', 'Unknown')

            cursor.execute(
                """
                INSERT INTO departures_connections 
                (from_station, to_station, vehicle, departure_time, arrival_time)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (from_station, to_station, vehicle, departure_time, arrival_time)
            )

        conn.commit()
        conn.close()

        return func.HttpResponse(
            f"Fetched {len(connections)} connections from {from_station} to {to_station}."
        )

    except Exception as e:
        logging.error(str(e))
        return func.HttpResponse(
            f"Error: {str(e)}",
            status_code=500
        )
