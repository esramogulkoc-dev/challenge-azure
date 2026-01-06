import logging
import requests
import pyodbc
import azure.functions as func

# ----------------------------
# SQL connection string
# ----------------------------
conn_str = "Driver={ODBC Driver 18 for SQL Server};Server=tcp:<server-name>.database.windows.net,1433;Database=<db-name>;Uid=<username>;Pwd=<password>;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Mevcut fetch kodu
    station = req.params.get('station')
    if not station:
        return func.HttpResponse("Please pass a station parameter", status_code=400)

    url = f"https://api.irail.be/liveboard/?station={station}&format=json&arrdep=departure&alerts=false"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        departures = data.get('departures', {}).get('departure', [])

        # ----------------------------
        # SQL insert kısmı
        # ----------------------------
        with pyodbc.connect(conn_str) as conn:
            cursor = conn.cursor()
            for train in departures:
                vehicle = train.get('vehicle')
                timestamp = train.get('time')
                cursor.execute("""
                    INSERT INTO departures_table (station, vehicle, timestamp)
                    VALUES (?, ?, ?)
                """, station, vehicle, timestamp)
            conn.commit()

    
        return func.HttpResponse(f"Fetched {len(departures)} departures for {station} and inserted into SQL.")

    except Exception as e:
        logging.error(str(e))
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)
