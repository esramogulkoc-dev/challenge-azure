import logging
import requests
import pymssql
import azure.functions as func

server = "sql-data-train-2026-1.database.windows.net"
database = "irail-db"
username = "esra-admin-sql"
password = "becode2026*"

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    station = req.params.get('station')
    if not station:
        return func.HttpResponse(
            "Please pass a station parameter, e.g. ?station=Brussels-Central",
            status_code=400
        )

    url = f"https://api.irail.be/liveboard/?station={station}&format=json&arrdep=departure&alerts=false"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        departures = data.get('departures', {}).get('departure', [])

        conn = pymssql.connect(
            server=server,
            user=username,
            password=password,
            database=database
        )
        cursor = conn.cursor()
        for train in departures:
            vehicle = train.get('vehicle')
            timestamp = train.get('time')
            cursor.execute(
                "INSERT INTO departures_liveboard (station, vehicle, timestamp) VALUES (%s, %s, %s)",
                (station, vehicle, timestamp)
            )
        conn.commit()
        conn.close()

        return func.HttpResponse(f"Fetched {len(departures)} departures for {station} and inserted into SQL.")

    except Exception as e:
        logging.error(str(e))
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)
