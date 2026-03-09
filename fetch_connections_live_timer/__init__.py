import logging
import requests
import pymssql
import os
import azure.functions as func
import time

server = os.environ["SQL_SERVER"]
database = os.environ["SQL_DATABASE"]
username = os.environ["SQL_USERNAME"]
password = os.environ["SQL_PASSWORD"]

STATIONS = ["Leuven", "Gent-Sint-Pieters", "Brussels-Central", "Antwerp"]

def main(mytimer: func.TimerRequest) -> None:
    logging.info("Live connections timer started")

    now = int(time.time())
    two_hours_later = now + 2 * 3600

    conn = pymssql.connect(server, username, password, database)
    cursor = conn.cursor()

    # 🔥 LIVE tabloyu temizle
    cursor.execute("TRUNCATE TABLE departures_connections_live")

    for from_station in STATIONS:
        for to_station in STATIONS:
            if from_station == to_station:
                continue

            url = (
                f"https://api.irail.be/connections/"
                f"?from={from_station}&to={to_station}&format=json&alerts=false"
            )

            response = requests.get(url)
            data = response.json()

            for c in data.get("connection", []):
                dep = int(c["departure"]["time"])
                arr = int(c["arrival"]["time"])

                # ⏱ SADECE YAKIN ZAMAN
                if now <= dep <= two_hours_later:
                    cursor.execute(
                        """
                        INSERT INTO departures_connections_live
                        (from_station, to_station, vehicle, departure_time, arrival_time)
                        VALUES (%s, %s, %s, %s, %s)
                        """,
                        (
                            from_station,
                            to_station,
                            c.get("vehicle", "Unknown"),
                            dep,
                            arr
                        )
                    )

    conn.commit()
    conn.close()
    logging.info("Live connections table refreshed")
