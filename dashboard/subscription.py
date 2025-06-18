"""Module for handling user subscriptions."""

import logging

from boto3 import client
from streamlit import toast

logger = logging.getLogger(__name__)

logging.basicConfig(
    level="DEBUG",
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S"
)


def get_sns_client() -> client:
    """Return a SNS client."""
    logger.info("Creating SNS client...")
    sns = client("sns")
    return sns


def create_topic_name(latitude: float, longitude: float,
                      radius: int, magnitude: float) -> str:
    """Creates a topic name based on the provided information."""
    logger.info("Starting topic name creation...")
    magnitude = int(round(magnitude, 1)*10)
    latitude = format_coordinate(latitude)
    longitude = format_coordinate(longitude)
    return f"c17-quake-{magnitude}-{latitude}-{longitude}-{radius}"


def format_coordinate(coordinate: float) -> str:
    """Returns a formatted string of the latitude / longitude coordinate."""
    logger.info("Formatting coordinate...")
    if coordinate < 0:
        return f"m{int(round(coordinate * -1, 4)*10000)}"
    return f"p{int(round(coordinate, 4)*10000)}"


def create_topic(sns: client, topic_name: str) -> str:
    """Creates a topic and returns the TopicARN."""
    logger.info("Creating topic %s.", topic_name)
    return sns.create_topic(Name=topic_name)["TopicArn"]


def sub_to_topic(sns: client, topic_arn: str, email: str) -> None:
    """Subscribes a user to a topic based on the TopicArn."""
    logger.info("Subscribing %s to topic %s.", email, topic_arn)
    sns.subscribe(TopicArn=topic_arn,
                  Protocol="email",
                  Endpoint=email)


def make_subscription(email: str, latitude: float, longitude: float,
                      radius: int, magnitude: float) -> None:
    """Create a subscription to a topic for their preference.
    format: c17-quake-<magnitude>-(p/m)<latitude>-(p/m)<longitude>-<radius>"""
    logger.info("Starting subscription creation...")
    topic_name = create_topic_name(latitude, longitude, radius, magnitude)
    sns = get_sns_client()
    topic_arn = create_topic(sns, topic_name)
    sub_to_topic(sns, topic_arn, email)
    logger.info("Subscription has been completed.")
    toast("Subscription has been made!")
