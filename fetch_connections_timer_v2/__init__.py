import logging
import requests
import pymssql
import os
from datetime import datetime
import azure.functions as func

def main(mytimer: func.TimerRequest) -> None:
    server = os.environ.get("SQL_SERVER")
    database = os.environ.get("SQL_DATABASE")
    username = os.environ.get("SQL_USERNAME")
    password = os.environ.get("SQL_PASSWORD")

    # Analiz etmek istediğimiz ana istasyonlar
    stations = ["Leuven", "Brussels-Central", "Gent-Sint-Pieters", "Antwerpen-Centraal"]
    # Tüm kombinasyonları oluştur (Nereden-Nereye)
    routes = [(f, t) for f in stations for t in stations if f != t]
    
    conn = None

    try:
        conn = pymssql.connect(server=server, user=username, password=password, database=database)
        cursor = conn.cursor()

        for fr, to in routes:
            url = f"https://api.irail.be/connections/?from={fr}&to={to}&format=json"
            response = requests.get(url, timeout=10)
            data = response.json()
            connections = data.get('connection', [])

            for c in connections:
                # Zaman Dönüşümleri
                dep_dt = datetime.fromtimestamp(int(c['departure']['time']))
                arr_dt = datetime.fromtimestamp(int(c['arrival']['time']))
                
                # Süre Hesaplama (Saniye -> Dakika)
                duration = int(c.get('duration', 0)) // 60
                
                occupancy = c.get('occupancy', {}).get('name', 'unknown')
                vehicle = c['departure'].get('vehicle')

                # Aynı trenin aynı saatteki kaydı varsa tekrar ekleme
                cursor.execute("""
                    IF NOT EXISTS (SELECT 1 FROM departures_connections_4stations WHERE vehicle=%s AND departure_time=%s)
                    INSERT INTO departures_connections_4stations (from_station, to_station, vehicle, departure_time, arrival_time, duration_minutes, occupancy)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (vehicle, dep_dt, fr, to, vehicle, dep_dt, arr_dt, duration, occupancy))

        conn.commit()
        logging.info("Connections güncellemesi başarıyla tamamlandı (train-info-db).")
    except Exception as e:
        logging.error(f"Connections Hatası: {str(e)}")
    finally:
        if conn:
            conn.close()