import logging
import requests
import pymssql
import os
import azure.functions as func

server = os.environ.get("SQL_SERVER")
database = os.environ.get("SQL_DATABASE")
username = os.environ.get("SQL_USERNAME")
password = os.environ.get("SQL_PASSWORD")

def main(mytimer: func.TimerRequest) -> None:
    logging.info('fetch_liveboard_timer ran.')

    stations = ["Brussels-Central", "Leuven", "Gent-Sint-Pieters"]

    for station in stations:
        url = f"https://api.irail.be/liveboard/?station={station}&format=json&arrdep=departure&alerts=false"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            departures = data.get('departures', {}).get('departure', [])

            conn = pymssql.connect(server=server, user=username, password=password, database=database)
            cursor = conn.cursor()

            for train in departures:
                vehicle = train.get('vehicle')
                timestamp = train.get('time')

                cursor.execute("""
                    IF NOT EXISTS (SELECT 1 FROM departures_liveboard WHERE station=%s AND vehicle=%s AND timestamp=%s)
                    INSERT INTO departures_liveboard (station, vehicle, timestamp)
                    VALUES (%s, %s, %s)
                """, (station, vehicle, timestamp, station, vehicle, timestamp))

            conn.commit()
            conn.close()
        except Exception as e:
            logging.error(f"Error fetching liveboard for {station}: {str(e)}")
