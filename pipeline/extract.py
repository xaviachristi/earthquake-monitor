"""
Connects to the USGS earthquake API and extracts the
information into a Pandas DataFrame.
"""
"""
Important note [to add as an 'improvement' ticket]:
ObsPy is probably unnecessary for this script now.
Its API call could be handled without importing
a big library, most of which we will not use.
"""


import logging
import json
from datetime import datetime, timedelta
import re
import asyncio

import pandas as pd
from obspy import Catalog
from obspy.clients.fdsn import Client
from obspy.clients.fdsn.header import FDSNNoDataException
from aiohttp import ClientSession
from aiohttp.client_exceptions import ContentTypeError


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


def read_json(filename: str) -> dict:
    """Reads the local JSON files of earthquake data into a dataframe."""

    logger.info("Reading catalog JSON.")

    with open(filename, encoding="utf-8") as f:
        data = json.load(f)

    return data


def get_event_ids_from_json_list(event_summaries: list[dict]) -> list[str]:
    """Searches through a list of JSON entries and returns all the event IDs."""
    logger.info("Searching for event IDs.")
    event_ids = []
    for event in event_summaries:
        event_ids.append(re.search(r"(?<=eventid=)\w+", event["resource_id"]).group(0))
    return event_ids


def create_usgs_urls_from_event_ids(event_ids: list[str]) -> list[str]:
    """Returns a list of geojson IDs for the USGS earthquake API."""
    # Ideally this would be made generic but I'm not familiar with how
    # the other APIs work.

    logger.info("Constructing URLs.")

    urls = []
    for an_id in event_ids:
        urls.append(
            f"https://earthquake.usgs.gov/earthquakes/feed/v1.0/detail/{an_id}.geojson")

    return urls


async def make_api_call(session: ClientSession, url: str) -> dict:
    """Makes a single API call."""
    logger.debug("Making an API call to %s", url)

    response = await session.get(url)
    try:
        html = await response.json()
    except ContentTypeError as e:
        logger.error("URL %s caused Content Type Error: %s", url, e.status)
        logger.debug("Error message: %s", e.message)

    if response.status == 200:
        logger.info("Successful API call (status == 200).")
        return html


async def make_many_api_calls(urls: list[str]) -> list[dict]:
    """Makes many API calls."""

    logger.info("Beginning API calls.")

    async with ClientSession() as session:
        api_calls = [make_api_call(session, url) for url in urls]
        responses = await asyncio.gather(*api_calls)

    return responses


def extract(api: str, temp_file_name:str,
            start_time: datetime, end_time: datetime) -> list[dict]:
    """Calls the specified API and returns a list of detailed information."""

    try:
        res = access_api(api, start_time, end_time)

    except FDSNNoDataException:
        logger.info("No information for the time period.")
        return False
    
    write_catalog_as_json(temp_file_name, res)
    summary_json = read_json(temp_file_name)
    ids = get_event_ids_from_json_list(summary_json["events"])
    urls = create_usgs_urls_from_event_ids(ids)
    responses = asyncio.run(make_many_api_calls(urls))

    return responses


if __name__ == "__main__":
    # extract("USGS", datetime.now() - timedelta(weeks=2), datetime.now())

    extract("USGS", "temp_earthquake_data.json",
            datetime.now() - timedelta(days=1), datetime.now())
