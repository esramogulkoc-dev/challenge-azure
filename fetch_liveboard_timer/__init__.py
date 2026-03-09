import logging
import requests
import pymssql
import os
from datetime import datetime
import azure.functions as func

def main(mytimer: func.TimerRequest) -> None:
    # Azure Configuration'dan bilgileri al
    server = os.environ.get("SQL_SERVER")
    database = os.environ.get("SQL_DATABASE")
    username = os.environ.get("SQL_USERNAME")
    password = os.environ.get("SQL_PASSWORD")

    stations = ["Brussels-Central", "Leuven", "Gent-Sint-Pieters", "Antwerpen-Centraal"]
    conn = None

    try:
        conn = pymssql.connect(server=server, user=username, password=password, database=database)
        cursor = conn.cursor()

        for station in stations:
            url = f"https://api.irail.be/liveboard/?station={station}&format=json&arrdep=departure&lang=en"
            response = requests.get(url, timeout=10)
            data = response.json()
            departures = data.get('departures', {}).get('departure', [])

            for train in departures:
                vehicle = train.get('vehicle')
       
                dep_time = datetime.fromtimestamp(int(train.get('time')))
                delay = int(train.get('delay', 0)) // 60
                canceled = int(train.get('canceled', 0))

                # Mükerrer kaydı önleyen akıllı SQL sorgusu
                cursor.execute("""
                    IF NOT EXISTS (SELECT 1 FROM departures_liveboard WHERE vehicle=%s AND departure_time=%s)
                    INSERT INTO departures_liveboard (station, vehicle, departure_time, delay_minutes, is_canceled)
                    VALUES (%s, %s, %s, %s, %s)
                """, (vehicle, dep_time, station, vehicle, dep_time, delay, canceled))
        
        conn.commit()
        logging.info("Liveboard güncellemesi başarıyla tamamlandı (train-info-db).")
    except Exception as e:
        logging.error(f"Hata oluştu: {str(e)}")
    finally:
        if conn:
            conn.close()