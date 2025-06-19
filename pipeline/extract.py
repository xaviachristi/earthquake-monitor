"""
Extracts earthquake data from the USGS API and returns detailed event information.
"""
import logging
import json
from datetime import datetime, timedelta
import asyncio

import requests
from aiohttp import ClientSession
from aiohttp.client_exceptions import ContentTypeError

logger = logging.getLogger(__name__)

logging.basicConfig(
    level="DEBUG",
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S"
)


def access_api(start: datetime, end: datetime) -> dict:
    """Fetches earthquake events from the USGS API as a JSON object."""
    base_url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
    params = {
        "format": "geojson",
        "starttime": start.strftime("%Y-%m-%dT%H:%M:%S"),
        "endtime": end.strftime("%Y-%m-%dT%H:%M:%S"),
        "eventtype": "earthquake"
    }

    logger.info("Requesting events from USGS API.")
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    return response.json()


def get_event_ids_from_json_list(event_features: list[dict]) -> list[str]:
    """Extracts USGS event IDs from GeoJSON features."""
    logger.info("Extracting event IDs from GeoJSON.")
    return [feature["id"] for feature in event_features]


def create_usgs_urls_from_event_ids(event_ids: list[str]) -> list[str]:
    """Constructs detail URLs from USGS event IDs."""
    logger.info("Creating USGS detail URLs.")
    return [
        f"https://earthquake.usgs.gov/earthquakes/feed/v1.0/detail/{event_id}.geojson"
        for event_id in event_ids
    ]


async def make_api_call(session: ClientSession, url: str) -> dict:
    """Makes a single async API call to fetch event details."""
    logger.debug("Making API call to %s", url)
    response = await session.get(url)

    try:
        data = await response.json()
    except ContentTypeError as e:
        logger.error("URL %s caused Content Type Error: %s", url, e.status)
        return {}

    if response.status == 200:
        logger.info("Successful API call: %s", url)
        return data
    return {}


async def make_many_api_calls(urls: list[str]) -> list[dict]:
    """Makes multiple async API calls and returns list of results."""
    logger.info("Fetching detailed event data from USGS.")
    async with ClientSession() as session:
        tasks = [make_api_call(session, url) for url in urls]
        return await asyncio.gather(*tasks)


def extract(api: str, start_time: datetime, end_time: datetime) -> list[dict]:
    """Main extract function to retrieve and return detailed earthquake data."""
    if api.upper() != "USGS":
        raise ValueError("Only 'USGS' API is supported currently.")

    try:
        summary_json = access_api(start_time, end_time)
    except requests.exceptions.RequestException as e:
        logger.warning("No data returned or API error: %s", e)
        return []

    ids = get_event_ids_from_json_list(summary_json["features"])
    urls = create_usgs_urls_from_event_ids(ids)
    responses = asyncio.run(make_many_api_calls(urls))

    return responses


if __name__ == "__main__":
    extract("USGS", "/tmp/temp_earthquake_data.json",
            datetime.now() - timedelta(days=1), datetime.now())
