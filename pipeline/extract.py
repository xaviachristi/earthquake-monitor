"""
Connects to the USGS earthquake API and converts the information
into a Pandas DataFrame.
"""

import logging

import pandas as pd
import obspy


logger = logging.getLogger(__name__)

logging.basicConfig(
    level="WARNING",
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S"
)


def access_api(url: str) -> obspy.Catalog:
    """Calls the API, returning its data in a Catalog."""
    pass


def convert_catalog_to_dataframe(catalog: obspy.Catalog) -> pd.DataFrame:
    """Converts an ObsPy catalog to a DataFrame."""
    pass
