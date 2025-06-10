"""
Connects to the USGS earthquake API and converts the information
into a Pandas DataFrame.
"""

import logging
import json
from datetime import datetime

import pandas as pd
from obspy import Catalog
import obspy.clients.fdsn
import obspy.io.json


logger = logging.getLogger(__name__)

logging.basicConfig(
    level="DEBUG",
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S"
)


def access_api(api_base_url: str,) -> Catalog:
    """Calls the API, returning its data in a Catalog."""

    logger.info("Connecting to the API: %s", api_base_url)
    client = obspy.clients.fdsn.Client(api_base_url)

    logger.debug("API client:\n%s",client)

    logger.info("Retrieving events from API: %s", api_base_url)
    return client.get_events()


def convert_catalog_to_dataframe(catalog: Catalog) -> pd.DataFrame:
    """Converts an ObsPy catalog to a DataFrame."""

    logger.info("Converting catalog to dataframe.")

    catalog.write("test_write.json", format="JSON")


if __name__ == "__main__":

    # res = access_api("USGS")
    # print(convert_catalog_to_dataframe(res))

    # data = pd.read_json("test_write.json")
    with open("test_write.json", encoding="utf-8") as f:
        data = json.load(f)
        df = pd.json_normalize(data["events"], max_level=3)
        print(df)
        print(df.info())


        # Checklist for this data (this checklist may be outdated, depending on the ERD):

        # - magnitude
        print(df["magnitudes"]) # A dictionary containing magnitude information.
        # - time
        # - latitude
        # - longitude
        # - depth
        # - url
        print(df["origins"]) # A list of dictionaries containing:
                # URL & time;
                # Longitude;
                # Latitude;
                # Depth;
                # and others which are mostly irrelevant and include a lot of nulls.
        # - updated
        # - tsunami
        # - type
        print(df["event_type"]) # From what I can see, mostly "earthquake"!

    # Extract these here or in transform?
    # I would assume Transform is expecting a cleaner dataframe?
