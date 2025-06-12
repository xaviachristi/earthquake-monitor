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
    - JSON Normalise might be slow but so might flattening everything.
    - I already have function signatures for the initial plan.
    - JSON normalise might require the data to be in a JSON format.
    - JSON normalise feels like the 'proper' way of doing it.
    - Writing the code for flattening may take a while
        - There are example scripts I could base it off online.
    - JSON normalise is already being run in extract.py.
        - If I was to go with the alternative plan, I think  it would make
          more sense to adapt that script.
    - Flattening all the data will create A LOT of columns.

    If I had a list of all the columns I need (ERD + those used for filtering)
    and where they are (look at the JSON),
    I could use this to build arguments for pd.json_normalize().
        Does pd.json_normalize() require every key:value be mapped to a column? I doubt it?
    But I would have to experiment with pd.json_normalize() first.

    I need the location of the data for both methods, so I'm going to start by doing this.

    Required columns:       Location in raw JSON:                                   Location in DataFrame:
                                                                                    (Not written properly as they're lists of dicts)
    - magnitude             - {"events":[{"magnitudes":[("mag":HERE)]}]}            - df["magnitudes"["mag"]]
    - latitude              - {"events":["origins":[{"latitude":HERE}]]}            - df["origins"["latitude"]]
    - longitude             - {"events":["origins":[{"longitude":HERE}]]}           - df["origins"["longitude"]]
    - time                  - {"events":["origins":[{"time":HERE}]]}                - df["origins"["time"]]
    - updated               - Potentially creation_info.creation_time?
    - depth                 - {"events":["origins":[{"depth":HERE}]]}               - df["origins"["depth"]]
    - url                   - {"events":["resource_id":HERE]}                       - df["resource_id"]
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
    - state                 - They won't all be in the US (uncertain)? They won't all be in a state (certain).
    - TYPE                  - {"events":["event_type":HERE]}                        - df["event_type"]
    - DELETED?              - ?
    - REVIEWED?             - {"events":["origins":[{"evaluation_mode":HERE}]]}     - df["origins"]["evaluation_mode"]

    Will I have to join additional information from resource_id (I think Ruy mentioned this)?
    Do we *need* all these columns? What are they used for?
    For the MVP I suggest magnitude, long/lat/depth, time, url.
    We could keep other columns as optional and fill them in later or we could remove them?
    I think it's nice data to have but is going to take a long time to join it from the resource_id.

"""

import json
import logging
from datetime import datetime, timedelta
import pandas as pd


logger = logging.getLogger(__name__)

logging.basicConfig(
    level="DEBUG",
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S"
)


def make_row_for_dataframe(event: dict) -> list:
    """
    Returns a list containing all the information needed for the dataframe
    which load requires.
    """
    df_row = []
    # earthquake_id - creates a list incase there are multiple IDs.
    df_row.append(list(filter(None, event["properties"]["ids"].split(","))))
    # magnitude - 
    df_row.append(event[""])
    # "latitude",
    df_row.append(event[""])
    # "longitude",
    df_row.append(event[""])
    # "time",
    df_row.append(event[""])
    # "updated",
    df_row.append(event[""])
    # "depth",
    df_row.append(event[""])
    # "url",
    df_row.append(event[""])
    # "felt",
    df_row.append(event[""])
    # "tsunami",
    df_row.append(event[""])
    # "cdi",
    df_row.append(event[""])
    # "mmi",
    df_row.append(event[""])
    # "nst",
    df_row.append(event[""])
    # "sig",
    df_row.append(event[""])
    # "net",
    df_row.append(event[""])
    # "dmin",
    df_row.append(event[""])
    # "alert",
    df_row.append(event[""])
    # "location_source",
    df_row.append(event[""])
    # "magnitude_type",
    df_row.append(event[""])
    # "state_name",
    df_row.append(event[""])
    # "region_name"
    df_row.append(event[""])
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
    pass


def flatten_data(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out


if __name__ == "__main__":
    # extract("USGS", datetime.now() - timedelta(weeks=2), datetime.now())

    # file_name = "temp_earthquake_data.json"

    # df = read_json_to_dataframe(file_name)

    # print(df)
    # print(df.info)

    # print("Flat!")

    # with open(file_name, encoding="utf-8") as f:
    #     data = json.load(f)
    #     # This should be .apply/.map then json_normalize
    #     flattened_data = flatten_data(data["events"])
    #     df = pd.DataFrame([flattened_data])

    # print(df)
    # print(df.info)
    pass
