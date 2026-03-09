import logging
import requests
import pymssql
import os
import azure.functions as func

server = os.environ.get("SQL_SERVER")
database = os.environ.get("SQL_DATABASE")
username = os.environ.get("SQL_USERNAME")
password = os.environ.get("SQL_PASSWORD")

ALL_STATIONS = ["Leuven", "Gent-Sint-Pieters", "Brussels-Central", "Antwerp"]

def main(mytimer: func.TimerRequest) -> None:
    logging.info('--- Connection Timer v2 Başladı ---')

    # Rota kombinasyonlarını oluşturuyoruz
    routes = [(f, t) for f in ALL_STATIONS for t in ALL_STATIONS if f != t]
    conn = None

    try:
        conn = pymssql.connect(server=server, user=username, password=password, database=database, timeout=60)
        cursor = conn.cursor()
        total_inserted = 0

        for from_station, to_station in routes:
            url = f"https://api.irail.be/connections/?from={from_station}&to={to_station}&format=json&alerts=false"
            try:
                response = requests.get(url, timeout=15)
                response.raise_for_status()
                data = response.json()
                connections = data.get('connection', [])

                for conn_item in connections:
                    departure_time = conn_item.get('departure', {}).get('time')
                    arrival_time = conn_item.get('arrival', {}).get('time')
                    vehicle = conn_item.get('vehicle', 'Unknown')

                    # Mevcut tablo ismine (departures_connections_4stations) sadık kalıyoruz
                    cursor.execute("""
                        IF NOT EXISTS (
                            SELECT 1 FROM departures_connections_4stations 
                            WHERE from_station=%s AND to_station=%s AND vehicle=%s AND departure_time=%s
                        )
                        INSERT INTO departures_connections_4stations 
                        (from_station, to_station, vehicle, departure_time, arrival_time)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (from_station, to_station, vehicle, departure_time,
                          from_station, to_station, vehicle, departure_time, arrival_time))
                    
                    if cursor.rowcount > 0:
                        total_inserted += 1

            except Exception as e_inner:
                logging.warning(f"Rota Hatası ({from_station}-{to_station}): {str(e_inner)}")

        conn.commit()
        logging.info(f"İşlem Tamam. Toplam {total_inserted} yeni bağlantı eklendi.")

    except Exception as e:
        logging.error(f"Kritik Hata: {str(e)}")
    finally:
        if conn:
            conn.close()