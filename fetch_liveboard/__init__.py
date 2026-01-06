import logging
import requests
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Fetching iRail liveboard data...')

    # URL parametresi: ?station=Brussels-Central
    station = req.params.get('station')
    if not station:
        station = "Gent-Sint-Pieters"  # Default station

    # iRail API URL
    url = f"https://api.irail.be/liveboard/?station={station}&format=json"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Şimdilik direkt JSON string olarak return ediyoruz
        return func.HttpResponse(
            str(data),
            mimetype="application/json",
            status_code=200
        )
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching iRail data: {e}")
        return func.HttpResponse(
            f"Error fetching data: {e}",
            status_code=500
        )
