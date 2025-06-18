"""Module for finding subscription topics."""

from datetime import datetime
from pytz import timezone
from logging import getLogger, basicConfig
from math import radians, cos, sin, sqrt, atan2
from re import search

from pandas import DataFrame
from boto3 import client

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
    r = 6371.0

    phi1 = radians(lat1)
    phi2 = radians(lat2)
    d_phi = radians(lat2 - lat1)
    d_lambda = radians(lon2 - lon1)

    a = sin(d_phi/2)**2 + cos(phi1) * cos(phi2) * sin(d_lambda/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = r * c
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
                    "time": row['time'].strftime(r"%Y-%m-%d %H:%M"),
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
            r'c17-quake-\d+-(m|p)\d+-(m|p)\d+-\d+', topic.get('TopicArn'))
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
        "magnitude": float(parts[2])/10,
        "latitude": float(lat[1:])/10000 if lat[0] == "p" else -float(lat[1:])/10000,
        "longitude": float(lon[1:])/10000 if lon[0] == "p" else -float(lon[1:])/10000,
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


if __name__ == "__main__":
    london_tz = timezone("Europe/London")
    sample_df = DataFrame([
        {
            "earthquake_id": 1,
            "magnitude": 5.7,
            "latitude": 12.45,
            "longitude": -47.15,
            "time": london_tz.localize(datetime.strptime("2024-02-01", "%Y-%m-%d")),
            "updated": london_tz.localize(datetime.strptime("2024-02-02", "%Y-%m-%d")),
            "depth": 5.0,
            "url": "example.com/1",
            "felt": 1,
            "tsunami": False,
            "cdi": 3.1,
            "mmi": 2.3,
            "nst": 1,
            "sig": 1,
            "net": "us",
            "dmin": 0.1,
            "alert": "green",
            "location_source": "us",
            "magnitude_type": "Mb",
            "state_name": "California",
            "region_name": "West Coast",
            "state_id": 12,
            "region_id": 4
        },
        {
            "earthquake_id": 2,
            "magnitude": 3.7,
            "latitude": 11.0,
            "longitude": 21.0,
            "time": london_tz.localize(datetime.strptime("2024-02-01", "%Y-%m-%d")),
            "updated": london_tz.localize(datetime.strptime("2024-02-02", "%Y-%m-%d")),
            "depth": 7.0,
            "url": "example.com/2",
            "felt": 0,
            "tsunami": True,
            "cdi": 2.8,
            "mmi": 2.1,
            "nst": 2,
            "sig": 2,
            "net": "us",
            "dmin": 0.2,
            "alert": "yellow",
            "location_source": "us",
            "magnitude_type": "Mb",
            "state_name": "Nevada",
            "region_name": "Southwest",
            "state_id": 13,
            "region_id": 4
        }
    ])
    print(get_topic_dictionaries(sample_df))
