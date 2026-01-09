import logging
import requests
import pymssql
import azure.functions as func
import os

server = os.environ.get("SQL_SERVER")
database = os.environ.get("SQL_DATABASE")
username = os.environ.get("SQL_USERNAME")
password = os.environ.get("SQL_PASSWORD")

ALL_STATIONS = ["Leuven", "Gent-Sint-Pieters", "Brussels-Central", "Antwerp"]

def main(mytimer: func.TimerRequest) -> None:
    logging.info('fetch_connection_timer_v2 ran.')

    stations_to_fetch = [(f, t) for f in ALL_STATIONS for t in ALL_STATIONS if f != t]

    total_inserted = 0
    for from_station, to_station in stations_to_fetch:
        url = f"https://api.irail.be/connections/?from={from_station}&to={to_station}&format=json&alerts=false"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            connections = data.get('connection', [])

            conn = pymssql.connect(server=server, user=username, password=password, database=database)
            cursor = conn.cursor()

            for conn_item in connections:
                departure_time = conn_item.get('departure', {}).get('time')
                arrival_time = conn_item.get('arrival', {}).get('time')
                vehicle = conn_item.get('vehicle', 'Unknown')

                cursor.execute("""
                    IF NOT EXISTS (
                        SELECT 1 FROM departures_connections_4stations 
                        WHERE from_station=%s AND to_station=%s AND vehicle=%s AND departure_time=%s
                    )
                    INSERT INTO departures_connections_4stations 
                    (from_station, to_station, vehicle, departure_time, arrival_time)
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    from_station, to_station, vehicle, departure_time,
                    from_station, to_station, vehicle, departure_time, arrival_time
                ))

            conn.commit()
            conn.close()
            total_inserted += len(connections)

        except Exception as e:
            logging.error(f"Error fetching connections for {from_station} → {to_station}: {str(e)}")

    logging.info(f"Total inserted connections this run: {total_inserted}")
