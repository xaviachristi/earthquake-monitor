"""Script for running full ETL pipeline as AWS lambda."""

from datetime import datetime, timedelta
from logging import getLogger, basicConfig
from os import environ as ENV
from math import radians, cos, sin, sqrt, atan2

from pandas import DataFrame
from dotenv import load_dotenv

from extract import extract
from transform import transform
from load import load


logger = getLogger(__name__)

basicConfig(
    level="DEBUG",
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S"
)


def get_haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great-circle distance between two points 
    on the Earth (specified in decimal degrees).
    Returns distance in kilometers.
    """
    R = 6371.0

    phi1 = radians(lat1)
    phi2 = radians(lat2)
    d_phi = radians(lat2 - lat1)
    d_lambda = radians(lon2 - lon1)

    a = sin(d_phi/2)**2 + cos(phi1) * cos(phi2) * sin(d_lambda/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance


def is_point_in_circle(point_lat, point_lon, center_lat, center_lon, radius_km):
    """
    Return True if the point (point_lat, point_lon) lies within radius_km
    of the center (center_lat, center_lon), else False.
    """
    distance = get_haversine_distance(
        point_lat, point_lon, center_lat, center_lon)
    return distance <= radius_km


def get_topic_dictionaries(data: DataFrame) -> list[dict]:
    """Return topic strings and value list for sending alerts."""


def run_pipeline(start: datetime = datetime.now() - timedelta(minutes=1),
                 end: datetime = datetime.now()) -> list[dict]:
    """Run ETL pipeline."""
    logger.info(
        "Found environment: %s, %s", ENV["DB_USER"], ENV["DB_HOST"], ENV["DB_NAME"])

    logger.info("Extracting data from API...")
    raw = extract("USGS", start, end)

    logger.info("Transforming data...")
    transformed = transform(raw)

    logger.info("Loading data to RDS...")
    uploaded = load(transformed)

    return uploaded


def lambda_handler(event, context):
    """
    Main Lambda Handler Function
    Parameters:
        event: Dict containing the lambda function event data
        context: lAMBDA RUNTIME CONTEXT
    Returns:
        Dict containing status message
    """
    try:
        logger.info("Running ETL pipeline...")
        data = run_pipeline()

        logger.info("Creating alert dictionary...")
        topics = get_topic_dictionaries(data)

        return {
            "statusCode": 200,
            "message": topics
        }
    except Exception as e:
        logger.error("Error running pipeline lambda: %s", str(e))
        raise RuntimeError("Python pipeline failed to execute: %s", e)


if __name__ == "__main__":
    load_dotenv()
    run_pipeline()
