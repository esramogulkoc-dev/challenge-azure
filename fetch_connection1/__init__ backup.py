import logging
import requests
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Query param: ?station=Brussels-Central
    station = req.params.get('station')
    if not station:
        return func.HttpResponse("Please pass a station parameter", status_code=400)

    # iRail API endpoint
    url = f"https://api.irail.be/liveboard/?station={station}&format=json&arrdep=departure&alerts=false"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Kaç tren geldiğini alalım
        num_departures = data.get('departures', {}).get('number', 0)

        return func.HttpResponse(f"Fetched {num_departures} departures for {station}")

    except Exception as e:
        logging.error(str(e))
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)
