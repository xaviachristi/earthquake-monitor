"""Script for running full ETL pipeline as AWS lambda."""

from datetime import datetime, timedelta
from logging import getLogger, basicConfig
from os import environ as ENV
from math import radians, cos, sin, sqrt, atan2
from re import search

from pandas import DataFrame
from dotenv import load_dotenv
from boto3 import client

from extract import extract
from transform import transform
from load import load


logger = getLogger(__name__)

basicConfig(
    level="DEBUG",
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S"
)


def get_client() -> client:
    """Return AWS SNS client"""
    return client('sns')


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
    logger.info("For point %s, %s and centre %s, %s distance is %s...",
                point_lat, point_lon, center_lat, center_lon, distance)
    return distance <= radius_km


def get_applicable_topics(topics: list[dict], row: dict) -> list[dict]:
    """Returns any topics that apply to this row of data."""
    subscribed_topics = []
    target_mag = row["magnitude"]
    target_lat = row["latitude"]
    target_long = row["longitude"]
    for t in topics:
        min_mag = t["magnitude"]
        centre_lat = t["latitude"]
        centre_long = t["longitude"]
        centre_radius = t["radius"]
        if target_mag >= min_mag:
            logger.info("Found topic with matching magnitude...")
            if is_point_in_circle(target_lat, target_long, centre_lat,
                                  centre_long, centre_radius):
                logger.info("Found topic with matching location...")
                subscribed_topics.append({
                    "topic_arn": t["topic_arn"],
                    "magnitude": target_mag,
                    "state_name": row["state_name"],
                    "region_name": row["region_name"],
                    "time": row["time"],
                    "tsunami": row["tsunami"],
                    "latitude": target_lat,
                    "longitude": target_long
                })
    return subscribed_topics


def get_topics(sns_client: client) -> list[dict]:
    """Return list of topic arns and names on SNS filtered for earthquake project."""
    arns = []
    topics = []
    response = sns_client.list_topics()
    next_token = response.get('NextToken', None)
    arns = response.get('Topics')
    logger.info("Found SNS Topics: %s", arns)
    while next_token:
        response = sns_client.list_topics(next_token)
        next_token = response.get('NextToken', None)
        arns.extend(response.get('Topics'))
    for topic in arns:
        topic_name = search(
            r'c17-quake-\d{1,2}-(m|p)\d{1,2}-(m|p)\d{1,2}-\d+', topic.get('TopicArn'))
        if topic_name:
            topics.append(get_dict_from_topic(
                topic_name.group(0), topic.get('TopicArn')))
    logger.info("Found earthquake topics: %s", topics)
    return topics


def get_dict_from_topic(name: str, arn: str) -> list[dict]:
    """Return dictionary from topic with seperated information."""
    parts = name.split("-")
    lat = parts[3]
    lon = parts[4]
    return {
        "topic_arn": arn,
        "magnitude": float(parts[2]),
        "latitude": float(lat[1:]) if lat[0] == "p" else float(-lat[1:]),
        "longitude": float(lon[1:]) if lon[0] == "p" else float(-lon[1:]),
        "radius": int(parts[5])
    }


def get_topic_dictionaries(data: DataFrame) -> list[dict]:
    """Return topic strings and value list for sending alerts."""
    output_topics = []
    sns_client = get_client()
    topics = get_topics(sns_client)
    logger.info("Extracted info from topics: %s", topics)
    for _, row in data.iterrows():
        target_topics = get_applicable_topics(topics, row.to_dict())
        logger.info("Found subscriber topics: %s", target_topics)
        if target_topics:
            output_topics.extend(target_topics)
    return output_topics


def run_pipeline(start: datetime = datetime.now() - timedelta(minutes=1),
                 end: datetime = datetime.now()) -> DataFrame:
    """Run ETL pipeline."""
    logger.info(
        "Found environment: %s, %s, %s", ENV["DB_USER"], ENV["DB_HOST"], ENV["DB_NAME"])

    logger.info("Extracting data from API...")
    raw = extract("USGS", "/tmp/temp_earthquake_data.json", start, end)
    if raw is False or not raw or len(raw) == 0:
        logger.warning("No data returned from API.")
        return None

    logger.info("Transforming data...")
    transformed = transform(raw)
    if transformed.empty:
        logger.warning("Failed to transform data returned from API.")
        return None
    logger.info("Transformed data into: %s", transformed)

    logger.info("Loading data to RDS...")
    uploaded = load(transformed)
    if uploaded.empty:
        logger.warning("No data uploaded to RDS.")
        return None
    logger.info("Loaded data into RDS: %s", uploaded)

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
        # data = run_pipeline(datetime.now() - timedelta(hours=1),
        #                    datetime.now())
        data = run_pipeline(datetime.now() - timedelta(hours=1),
                            datetime.now())

        topics = None

        if data is not None:
            if not data.empty:
                logger.info("Creating alert dictionary...")
                topics = get_topic_dictionaries(data)

        return {
            "statusCode": 200,
            "message": topics
        }
    except Exception as e:
        logger.error("Error running pipeline lambda", exc_info=True)
        raise RuntimeError(f"Python pipeline failed to execute: {e}") from e


if __name__ == "__main__":
    load_dotenv()
    run_pipeline(datetime.now() - timedelta(hours=2),
                 datetime.now())
