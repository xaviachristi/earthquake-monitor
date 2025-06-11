"""
Connects to the USGS earthquake API and extracts the
information into a Pandas DataFrame.
"""

import logging
import json
from datetime import datetime, timedelta

import pandas as pd
from obspy import Catalog
from obspy.clients.fdsn import Client
from obspy.clients.fdsn.header import FDSNNoDataException


logger = logging.getLogger(__name__)

logging.basicConfig(
    level="DEBUG",
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S"
)


def access_api(api_base_url: str, start: datetime, end: datetime) -> Catalog:
    """Calls the API, returning its data in a Catalog."""

    logger.info("Connecting to the API: %s", api_base_url)
    client = Client(api_base_url)

    logger.info("Retrieving events from %s to %s from the %s API.",
                start, end, api_base_url)
    return client.get_events(starttime=start, endtime=end)


def write_catalog_as_json(filename: str, catalog: Catalog) -> None:
    """Writes an ObsPy catalog into a local JSON file."""

    logger.info("Writing catalog JSON.")
    catalog.write(filename, format="JSON")


def read_json_to_dataframe(filename: str) -> pd.DataFrame:
    """Reads the local JSON files of earthquake data into a dataframe."""

    logger.info("Reading catalog JSON.")
    with open(filename, encoding="utf-8") as f:
        data = json.load(f)
        df = pd.json_normalize(data["events"], max_level=4)

    logger.debug("Dataframe information:\n%s", df.info())
    return df


def extract(api: str, start_time: datetime, end_time: datetime) -> pd.DataFrame:
    """Calls the specified API and returns a DataFrame of the information."""

    try:
        return convert_catalog_to_dataframe(access_api(api, start_time, end_time))

    except FDSNNoDataException:
        logger.info("No information for the time period.")
        return False


if __name__ == "__main__":
    extract("USGS", datetime.now() - timedelta(weeks=2), datetime.now())
