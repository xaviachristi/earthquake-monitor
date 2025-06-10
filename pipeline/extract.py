"""
Connects to the USGS earthquake API and converts the information
into a Pandas DataFrame.
"""

import logging
from datetime import datetime

import pandas as pd
from obspy import Catalog
import obspy.clients.fdsn


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

    logger.debug(client)

    logger.info("Retrieving events from API: %s", api_base_url)
    return client.get_events()


def convert_catalog_to_dataframe(catalog: Catalog) -> pd.DataFrame:
    """Converts an ObsPy catalog to a DataFrame."""
    pass


if __name__ == "__main__":

    print(access_api("USGS"))
