"""
Transforms a dataframe into a format appropriate for loading into the database.
"""
import logging
from datetime import datetime, timedelta
from os import environ as ENV

import pandas as pd
from dotenv import load_dotenv
from opencage.geocoder import OpenCageGeocode

from extract import extract


logger = logging.getLogger(__name__)

logging.basicConfig(
    level="INFO",
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S"
)


def is_event_in_correct_format(potential_event: dict) -> bool:
    """Checks that a potential event is a dictionary with the expected keys."""
    logger.debug("Checking for event format.")

    if not isinstance(potential_event, dict):
        return False

    try:
        potential_event["properties"]["ids"]
        potential_event["properties"]["type"]

    except KeyError as e:
        logger.error("Missing keys. Information: %s", str(e))
        return False

    return True


def is_event_clean(event: dict) -> bool:
    """Checks if we want an entry in the database."""
    logger.info("Checking if event is clean.")

    if not is_event_in_correct_format(event):
        return False

    if event["properties"]["type"] != "earthquake":
        logger.info("Unclean event found. ID: %s", event["properties"]["ids"])
        return False

    return True


def clean_earthquake_data(earthquake_data: list[dict]) -> list[dict]:
    """Removes entries that we don't want in the database."""
    logger.info("Removing unwanted events.")
    logger.info("Total events: %s.", len(earthquake_data))

    clean_events = []
    for entry in earthquake_data:
        logger.debug("Event:\n%s", entry)
        if is_event_clean(entry):
            logger.debug("Event is clean.")
            clean_events.append(entry)

    logger.info("Clean events: %s.", len(clean_events))
    return clean_events


def get_address(latitude: float, longitude: float) -> list[str]:
    """Uses OpenCage to convert coordinates into an address."""
    logger.info("Finding address for %s, %s using OpenCage.",
                latitude, longitude)
    try:
        geocoder = OpenCageGeocode(key=ENV["GEO_API_KEY"])
        results = geocoder.reverse_geocode(
            latitude, longitude, no_annotations=1, limit=1)
        if results and len(results):
            components = results[0]["components"]
            country = components.get("country", "No Country")
            state = components.get("state", "Unknown State")
            return [state, country]
        else:
            logger.warning("No results from OpenCage for %s, %s",
                           latitude, longitude)
            return ["Unknown", "No Country"]
    except Exception as e:
        logger.error("OpenCage error for coords (%s, %s): %s",
                     latitude, longitude, e)
        return ["Unknown", "No Country"]


def grab_state(address: list[str]) -> str:
    """Finds a state in an address."""
    logger.debug("Finding state inside address.")
    if not address[-2].isnumeric():
        return address[-2]
    return address[-3]


def get_region_from_state(state_name: str) -> str:
    """Looks up the a state name to find which region it is in."""
    return {"california": "West Coast",
            "oregon": "West Coast",
            "washington": "West Coast",

            "idaho": "Pacific Northwest",

            "nevada": "Southwest",
            "arizona": "Southwest",
            "new mexico": "Southwest",
            "texas": "Southwest",
            "oklahoma": "Southwest",
            "utah": "Southwest",

            "montana": "Rocky Mountains",
            "colorado": "Rocky Mountains",
            "wyoming": "Rocky Mountains",

            "north dakota": "Midwest",
            "south dakota": "Midwest",
            "nebraska": "Midwest",
            "kansas": "Midwest",
            "minnesota": "Midwest",
            "iowa": "Midwest",
            "missouri": "Midwest",
            "wisconsin": "Midwest",
            "illinois": "Midwest",
            "indiana": "Midwest",
            "michigan": "Midwest",
            "ohio": "Midwest",

            "arkansas": "Southeast",
            "louisiana": "Southeast",
            "kentucky": "Southeast",
            "tennessee": "Southeast",
            "mississippi": "Southeast",
            "alabama": "Southeast",
            "georgia": "Southeast",
            "florida": "Southeast",
            "south carolina": "Southeast",
            "north carolina": "Southeast",
            "virginia": "Southeast",
            "west virginia": "Southeast",

            "maryland": "Northeast",
            "delaware": "Northeast",
            "pennsylvania": "Northeast",
            "new jersey": "Northeast",
            "new york": "Northeast",
            "connecticut": "Northeast",
            "rhode island": "Northeast",
            "massachusetts": "Northeast",
            "vermont": "Northeast",
            "new hampshire": "Northeast",
            "maine": "Northeast",
            "district of columbia": "Northeast",

            "alaska": "Alaska",
            "hawaii": "Hawaii",
            "puerto rico": "Puerto Rico",
            "unknown state": "Unspecified United States"

            }[state_name.lower()]


def make_row_for_dataframe(event: dict) -> list:
    """
    Returns a list containing all the information needed for the dataframe
    which load requires.
    """
    logger.info(
        "Pulling relevant information out of the JSON data for one event.")
    df_row = []

    # earthquake_id - creates a list incase there are multiple IDs.
    df_row.append(list(filter(None, event["properties"]["ids"].split(","))))
    # Logged seperately to save repetition.
    logger.debug("Event ID: %s", df_row[0])
    # magnitude.
    df_row.append(event["properties"]["mag"])
    # latitude - origin is a list, hence the [0].
    df_row.append(event["properties"]["products"]
                  ["origin"][0]["properties"]["latitude"])
    # longitude.
    df_row.append(event["properties"]["products"]
                  ["origin"][0]["properties"]["longitude"])
    # time.
    df_row.append(event["properties"]["time"])
    # updated.
    df_row.append(event["properties"]["updated"])
    # depth.
    df_row.append(event["properties"]["products"]
                  ["origin"][0]["properties"]["depth"])
    # url.
    df_row.append(event["properties"]["url"])
    # felt.
    df_row.append(event["properties"]["felt"])
    # tsunami.
    df_row.append(event["properties"]["tsunami"])
    # cdi
    df_row.append(event["properties"]["cdi"])
    # mmi
    df_row.append(event["properties"]["mmi"])
    # nst
    df_row.append(event["properties"]["nst"])
    # sig
    df_row.append(event["properties"]["sig"])
    # net
    df_row.append(event["properties"]["net"])
    # dmin
    df_row.append(event["properties"]["dmin"])
    # alert
    df_row.append(event["properties"]["alert"])
    # location_source
    df_row.append(
        list(filter(None, event["properties"]["sources"].split(","))))
    # magnitude_type
    df_row.append(event["properties"]["magType"])
    # state_name - default: "Not in the USA".
    # region_name - if not in the USA, country name.
    address = get_address(df_row[2], df_row[3])
    if address[-1] == "United States":
        state = grab_state(address)
        df_row.append(state)
        df_row.append(get_region_from_state(state))
    else:
        df_row.append("Not in the USA")
        df_row.append(address[-1])

    return df_row


def create_dataframe_expected_for_load() -> pd.DataFrame:
    """
    Creates a dataframe with the columns expected for the load script.
    """
    return pd.DataFrame(columns=["earthquake_id", "magnitude", "latitude",
                        "longitude", "time", "updated", "depth", "url",
                                 "felt", "tsunami", "cdi", "mmi", "nst", "sig",
                                 "net", "dmin", "alert", "location_source",
                                 "magnitude_type", "state_name", "region_name"
                                 ])


def transform(data_from_extract: list[dict]) -> pd.DataFrame:
    """Cleans and reorganises the earthquake data from extract.py."""

    earthquakes = clean_earthquake_data(data_from_extract)

    df = create_dataframe_expected_for_load()

    for i in range(len(earthquakes)):

        df.loc[i] = make_row_for_dataframe(earthquakes[i])

    return df


if __name__ == "__main__":
    load_dotenv()
    events = extract("USGS", "temp_earthquake_data.json",
                     datetime.now() - timedelta(hours=4), datetime.now())
    events_dataframe = transform(events)
    print(events_dataframe)
    print(events_dataframe.info())
