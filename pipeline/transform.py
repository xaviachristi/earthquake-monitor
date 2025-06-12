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


import logging
from datetime import datetime, timedelta
from json import loads

import pandas as pd
from geopy.geocoders import Nominatim


logger = logging.getLogger(__name__)

logging.basicConfig(
    level="INFO",
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S"
)

def is_event_clean(event: dict) -> bool:
    """Checks if we want an entry in the database."""
    if event["properties"]["status"] != "reviewed":
        return False


def clean_earthquake_data(earthquake_data: list[dict]) -> list[dict]:
    """Removes entries that we don't want in the database."""
    pass


def get_address(latitude: float, longitude: float) -> str:
    """Calls GeoPy to convert coords into an address."""

    logger.info("Finding position %s, %s.", latitude, longitude)

    geolocator = Nominatim(user_agent="earthquake_monitor")

    return geolocator.reverse(f"{latitude}, {longitude}")[0].split(", ")


def grab_state(address: list[str])-> str:
    """Finds a state in an address."""
    if not address[-2].isnumeric():
        return address[-2]
    return address[-3]


def get_region_from_state(state_name: str) -> str:
    """Looks up the a state name to find which region it is in."""
    return {"california": "West Coast",
            "oregon": "West Coast",
            "washington'": "West Coast",
            
            "idaho": "Pacific Northwest",

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
            "puerto rico": "Puerto Rico"

    }[state_name.lower()]


def make_row_for_dataframe(event: dict) -> list:
    """
    Returns a list containing all the information needed for the dataframe
    which load requires.
    """

    df_row = []

    # earthquake_id - creates a list incase there are multiple IDs.
    df_row.append(list(filter(None, event["properties"]["ids"].split(","))))
    # magnitude.
    df_row.append(event["properties"]["mag"])
    # latitude - origin is a list, hence the [0].
    df_row.append(event["properties"]["products"]["origin"][0]["properties"]["latitude"])
    # longitude.
    df_row.append(event["properties"]["products"]["origin"][0]["properties"]["longitude"])
    # time.
    df_row.append(event["properties"]["time"])
    # updated.
    df_row.append(event["properties"]["updated"])
    # depth.
    df_row.append(event["properties"]["products"]["origin"][0]["properties"]["depth"])
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
    df_row.append(list(filter(None, event["properties"]["sources"].split(","))))
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
    pass


if __name__ == "__main__":
    single_event = loads("""{"type": "Feature","properties":{"mag":0.53,"place":"10 km SSW of Idyllwild, CA","time":1749655031680,"updated":1749675581157,"tz":null,"url":"https://earthquake.usgs.gov/earthquakes/eventpage/ci41182664","felt":null,"cdi":null,"mmi":null,"alert":null,"status":"reviewed","tsunami":0,"sig":4,"net":"ci","code":"41182664","ids":",ci41182664,","sources":",ci,","types":",nearby-cities,origin,phase-data,scitech-link,","nst":15,"dmin":0.06854,"rms":0.13,"gap":115,"magType":"ml","type":"earthquake","title":"M 0.5 - 10 km SSW of Idyllwild, CA","products":{"nearby-cities":[{"indexid":5431596,"indexTime":1749675579811,"id":"urn:usgs-product:ci:nearby-cities:ci41182664:1749675578440","type":"nearby-cities","code":"ci41182664","source":"ci","updateTime":1749675578440,"status":"UPDATE","properties":{"eventsource":"ci","eventsourcecode":"41182664","pdl-client-version":"Version 2.7.10 2021-06-21"},"preferredWeight":7,"contents":{"nearby-cities.json":{"contentType":"application/json","lastModified":1749675578000,"length":596,"url":"https://earthquake.usgs.gov/realtime/product/nearby-cities/ci41182664/ci/1749675578440/nearby-cities.json"}}}],"origin":[{"indexid":5431595,"indexTime":1749675578850,"id":"urn:usgs-product:ci:origin:ci41182664:1749675577830","type":"origin","code":"ci41182664","source":"ci","updateTime":1749675577830,"status":"UPDATE","properties":{"azimuthal-gap":"115","depth":"15.81","depth-type":"from location","error-ellipse-azimuth":"357","error-ellipse-intermediate":"768","error-ellipse-major":"1248","error-ellipse-minor":"552","error-ellipse-plunge":"75","error-ellipse-rotation":"10","evaluation-status":"final","event-type":"earthquake","eventParametersPublicID":"quakeml:service.scedc.caltech.edu/fdsnws/event/1/query?eventid=41182664","eventsource":"ci","eventsourcecode":"41182664","eventtime":"2025-06-11T15:17:11.680Z","horizontal-error":"0.31","latitude":"33.6663333","longitude":"-116.771","magnitude":"0.53","magnitude-azimuthal-gap":"123.5","magnitude-error":"0.206","magnitude-num-stations-used":"7","magnitude-source":"CI","magnitude-type":"ml","minimum-distance":"0.06854","num-phases-used":"28","num-stations-used":"15","origin-source":"CI","pdl-client-version":"Version 2.7.10 2021-06-21","quakeml-magnitude-publicid":"quakeml:service.scedc.caltech.edu/fdsnws/event/1/query?magnitudeid=109412373","quakeml-origin-publicid":"quakeml:service.scedc.caltech.edu/fdsnws/event/1/query?originid=105898557","quakeml-publicid":"quakeml:service.scedc.caltech.edu/fdsnws/event/1/query?eventid=41182664","review-status":"reviewed","standard-error":"0.13","title":"10 km SSW of Idyllwild, CA","version":"6","vertical-error":"0.51"},"preferredWeight":157,"contents":{"contents.xml":{"contentType":"application/xml","lastModified":1749675578000,"length":195,"url":"https://earthquake.usgs.gov/realtime/product/origin/ci41182664/ci/1749675577830/contents.xml"},"quakeml.xml":{"contentType":"application/xml","lastModified":1749675577000,"length":3423,"url":"https://earthquake.usgs.gov/realtime/product/origin/ci41182664/ci/1749675577830/quakeml.xml"}}}],"phase-data":[{"indexid":5431597,"indexTime":1749675580880,"id":"urn:usgs-product:ci:phase-data:ci41182664:1749675577830","type":"phase-data","code":"ci41182664","source":"ci","updateTime":1749675577830,"status":"UPDATE","properties":{"azimuthal-gap":"115","depth":"15.81","depth-type":"from location","error-ellipse-azimuth":"357","error-ellipse-intermediate":"768","error-ellipse-major":"1248","error-ellipse-minor":"552","error-ellipse-plunge":"75","error-ellipse-rotation":"10","evaluation-status":"final","event-type":"earthquake","eventParametersPublicID":"quakeml:service.scedc.caltech.edu/fdsnws/event/1/query?eventid=41182664","eventsource":"ci","eventsourcecode":"41182664","eventtime":"2025-06-11T15:17:11.680Z","horizontal-error":"0.31","latitude":"33.6663333","longitude":"-116.771","magnitude":"0.53","magnitude-azimuthal-gap":"123.5","magnitude-error":"0.206","magnitude-num-stations-used":"7","magnitude-source":"CI","magnitude-type":"ml","minimum-distance":"0.06854","num-phases-used":"28","num-stations-used":"15","origin-source":"CI","pdl-client-version":"Version 2.7.10 2021-06-21","quakeml-magnitude-publicid":"quakeml:service.scedc.caltech.edu/fdsnws/event/1/query?magnitudeid=109412373","quakeml-origin-publicid":"quakeml:service.scedc.caltech.edu/fdsnws/event/1/query?originid=105898557","quakeml-publicid":"quakeml:service.scedc.caltech.edu/fdsnws/event/1/query?eventid=41182664","review-status":"reviewed","standard-error":"0.13","title":"10 km SSW of Idyllwild, CA","version":"6","vertical-error":"0.51"},"preferredWeight":157,"contents":{"contents.xml":{"contentType":"application/xml","lastModified":1749675578000,"length":195,"url":"https://earthquake.usgs.gov/realtime/product/phase-data/ci41182664/ci/1749675577830/contents.xml"},"quakeml.xml":{"contentType":"application/xml","lastModified":1749675577000,"length":100216,"url":"https://earthquake.usgs.gov/realtime/product/phase-data/ci41182664/ci/1749675577830/quakeml.xml"}}}],"scitech-link":[{"indexid":5431598,"indexTime":1749675582101,"id":"urn:usgs-product:ci:scitech-link:ci41182664-waveform_ci:1749675581157","type":"scitech-link","code":"ci41182664-waveform_ci","source":"ci","updateTime":1749675581157,"status":"UPDATE","properties":{"addon-code":"Waveform_CI","addon-type":"LinkURL","eventsource":"ci","eventsourcecode":"41182664","pdl-client-version":"Version 2.7.10 2021-06-21","text":"Waveforms","url":"https://scedc.caltech.edu/review_eventfiles/makePublicView.html?evid=41182664","version":"01"},"preferredWeight":7,"contents":[]}]}},"geometry":{"type":"Point","coordinates":[-116.771,33.6663333,15.81]},"id":"ci41182664"}""")
    row = make_row_for_dataframe(single_event)

    df = create_dataframe_expected_for_load()
    df.loc[0] = row
    print(df)
    print(df.info())

    # Possible test cases for 
    # print(get_state_from_pos(33.6663333, -116.771))
    # print(get_state_from_pos(38.875807, -77.0309))
    # print(get_state_from_pos(38.98367794543014, -77.05994602599287))
    pass
