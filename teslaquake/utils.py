import requests
import logging

from datetime import date

from models import Event
from config import TESLAQUAKE_URL


def get_teslaquake_data(starttime: date, endtime: date):
    try:
        logging.info(f"Querying API from {starttime} to {endtime}...")

        params = {
            "format": "geojson",
            "starttime": starttime.strftime("%Y-%m-%d"),
            "endtime": endtime.strftime("%Y-%m-%d"),
        }

        response = requests.get(url=f"{TESLAQUAKE_URL}", params=params)
        response.raise_for_status()

    except requests.exceptions.HTTPError as e:
        logging.error(f"Querying API from {starttime} to {endtime} failed.", exc_info=e)
        raise e

    except requests.exceptions.RequestException as e:
        logging.error(f"Querying API from {starttime} to {endtime} failed.", exc_info=e)
        raise e

    logging.info(f"Querying API from {starttime} to {endtime} successful.")
    return response.json()


def convert_to_event(event_json) -> Event:

    event = Event(
        id        = event_json["id"],
        type      = event_json["properties"]["type"],
        place     = event_json["properties"]["place"],
        time      = event_json["properties"]["time"],
        latitude  = event_json["geometry"]["coordinates"][1],
        longitude = event_json["geometry"]["coordinates"][0],
        depth     = event_json["geometry"]["coordinates"][2],
        magType   = event_json["properties"]["magType"],
        mag       = event_json["properties"]["mag"],
    )

    return event
