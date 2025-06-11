"""
Transforms a dataframe into a format appropriate for loading into the database.
"""

"""
Initial plan:
    Flow of logic:
    1. Flatten out the nested data.
    2. Clean the data.
    3. Create a new dataframe with the correct columns and assign the
    cleaned and flattened data to it.

    The reason for flattening the data out is to make steps 2 and 3
    simpler and more consistent.

Alternative plan:
    1. Use pd.json_normalize() with a specified structure to pull the
       data straight into the format.
    2. Drop rows similar to initial plan.
    3. Drop and rename columns.

Advantages & Disadvantages:
    JSON Normalise might be slow but so might flattening everything.
    I already have function signatures for the initial plan.
    JSON normalise might require the data to be in a JSON format.
    JSON normalise feels like the 'proper' way of doing it.
    Writing the code for flattening may take a while
        There are example scripts I could base it off online.
    JSON normalise is already being run in extract.py.
        If I was to go with the alternative plan, I think  it would make
        more sense to adapt that script.
    Flattening the data will create A LOT of columns.

    If I had a list of all the columns I need (ERD + those used for filtering)
    and where they are (look at the JSON).
    I could use this to build arguments for pd.json_normalize().

    I need the location for either method, so I'm going to start by doing this.

    Required columns:       Location in raw JSON:                                   Location in DataFrame:
    - magnitude             - {"events":[{"magnitudes":[("mag":HERE)]}]}            - 
    - latitude              - {"events":["origins":[{"latitude":HERE}]]}            - 
    - longitude             - {"events":["origins":[{"longitude":HERE}]]}           - 
    - time                  - {"events":["origins":[{"time":HERE}]]}                - 
    - updated               - Potentially creation_info.creation_time?
    - depth                 - {"events":["origins":[{"depth":HERE}]]}               - 
    - url                   - {"events":["resource_id":HERE]}                       - 
    - felt                  - ?
    - tsunami               - ?
    - cdi                   - What is?
    - mmi                   - What is?
    - nst                   - What is?
    - sig                   - What is?
    - net                   - What is?
    - dmin                  - What is?
    - alert                 - ?
    - location_source       - What is?
    - magnitude_type        - What is?
    - state                 - They won't all be in the US?
    - TYPE                  - {"events":["event_type":HERE]}                        - 
    - DELETED?              - ?
    - REVIEWED?             - {"events":["origins":[{"evaluation_mode":HERE}]]}     - 

    Will I have to join additional information from resource_id (I think Ruy mentioned this)?
    Do we *need* all these columns? What are they used for?
    For the MVP I suggest magnitude, long/lat/depth, time, url
    We could keep other columns as optional and fill them in later or remove them?
    I think it's nice data to have but is going to take a long time to join it from the resource_id.

"""

import json
import logging
from datetime import datetime, timedelta
from extract import extract # For testing during development.
import pandas as pd


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
    # extract("USGS", datetime.now() - timedelta(weeks=2), datetime.now())

    filename = "temp_earthquake_data.json"

    logger.info("Reading catalog JSON.")

    with open(filename, encoding="utf-8") as f:
        data = json.load(f)
        df = pd.json_normalize(data["events"], max_level=3)

    # Checking that there's not an agreed upon format.
    # df = pd.read_json(filename, orient="split")

    print(df)
    logger.debug("Dataframe information:\n%s", df.info())
