"""
Transforms a dataframe into a format appropriate for loading into the database.

Flow of logic:
1. Flatten out the nested data.
2. Clean the data.
3. Create a new dataframe with the correct columns and assign the
   cleaned and flattened data to it.

The reason for flattening the data out is to make steps 2 and 3
simpler and more consistent.
"""

import logging
from datetime import datetime, timedelta

import pandas as pd

from extract import extract # For testing during development.


logger = logging.getLogger(__name__)

logging.basicConfig(
    level="DEBUG",
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S"
)


def flatten_nested_dictionary(nested_dictionary: pd.Series
                              ) -> pd.DataFrame:
    """
    Takes a column that has nested JSON dictionaries inside and converts them
    into unique columns.
    """
    """
    Initial thoughts: might be recursive (if multiple nested dictionaries).
    Should use the original column's name as a prefix.
    Might be able to use json_normalize() for this.
    """
    pass


def cleanse_earthquake_data(flattened_earthquake_data: pd.DataFrame
                            ) -> pd.DataFrame:
    """
    Drops rows that are not suitable for our database.
    This includes row that have:
    - non-earthquake type (i.e. quarrying readings)
    - not been reviewed
    - been marked as deleted
    """
    pass

def create_dataframe_expected_for_load(clean_earthquake_date: pd.DataFrame
                                       ) -> pd.DataFrame:
    """
    Creates a dataframe with the columns expected for the load script,
    using the cleaned earthquake data.
    """
    pass

def transform(dataframe_from_extract: pd.DataFrame) -> pd.DataFrame:
    """Cleans and reorganises the earthquake data from extract.py."""
    pass


if __name__ == "__main__":
    extract("USGS", datetime.now() - timedelta(weeks=2), datetime.now())
