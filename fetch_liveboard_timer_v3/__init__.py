import logging
import requests
import pymssql
import os
import azure.functions as func

# Konfigürasyonlar
server = os.environ.get("SQL_SERVER")
database = os.environ.get("SQL_DATABASE")
username = os.environ.get("SQL_USERNAME")
password = os.environ.get("SQL_PASSWORD")

def main(mytimer: func.TimerRequest) -> None:
    logging.info('--- Liveboard Timer Başladı ---')
    
    stations = ["Brussels-Central", "Leuven", "Gent-Sint-Pieters"]
    conn = None

    try:
        # Bağlantıyı döngü dışında bir kez açıyoruz
        conn = pymssql.connect(server=server, user=username, password=password, database=database, timeout=30)
        cursor = conn.cursor()

        for station in stations:
            url = f"https://api.irail.be/liveboard/?station={station}&format=json&arrdep=departure&alerts=false"
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                data = response.json()
                departures = data.get('departures', {}).get('departure', [])

                for train in departures:
                    vehicle = train.get('vehicle')
                    timestamp = train.get('time') # Mevcut tablon timestamp beklediği için çevirmedik

                    # Mevcut tablo yapına sadık kalarak Tekilleştirme (Deduplication)
                    cursor.execute("""
                        IF NOT EXISTS (SELECT 1 FROM departures_liveboard WHERE station=%s AND vehicle=%s AND timestamp=%s)
                        INSERT INTO departures_liveboard (station, vehicle, timestamp)
                        VALUES (%s, %s, %s)
                    """, (station, vehicle, timestamp, station, vehicle, timestamp))

            except Exception as e_inner:
                logging.error(f"İstasyon Hatası ({station}): {str(e_inner)}")

        conn.commit()
        logging.info("Liveboard verileri başarıyla işlendi.")

    except Exception as e:
        logging.error(f"Bağlantı veya SQL Hatası: {str(e)}")
    finally:
        if conn:
            conn.close()
            logging.info("Bağlantı güvenli şekilde kapatıldı.")