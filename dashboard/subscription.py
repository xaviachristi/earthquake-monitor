"""Module for handling user subscriptions."""

import logging
from os import environ as ENV

from dotenv import load_dotenv
from boto3 import client

logger = logging.getLogger(__name__)

logging.basicConfig(
    level="DEBUG",
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S"
)


def get_sns_client() -> client:
    """Return a SNS client."""
    sns = client("sns", aws_access_key_id=ENV["AWS_ACCESS_KEY"],
                 aws_secret_access_key=ENV["AWS_SECRET_ACCESS_KEY"])
    return sns


def delete_subscription():
    """Remove subscription to topic from SNS."""


def view_subscription():
    """Display information about subscribed topic."""


def make_subscription(first_name: str, last_name: str, email: str,
                      latitude: float, longitude: float, radius: int, magnitude: float) -> None:
    """Create a subscription to a topic for their preference.
    format: c17-quake-<magnitude>-(p/m)<latitude>-(p/m)<longitude>-<radius>"""
    topic_name = "c17-quake"
    topic_name = create_topic_name(
        topic_name, latitude, longitude, radius, magnitude)
    sns = get_sns_client()
    topic_arn = create_topic(sns, topic_name)
    sub_to_topic(sns, topic_arn, email)


def create_topic_name(topic_name: str, latitude: float, longitude: float,
                      radius: int, magnitude: float) -> str:
    """Creates a topic name based on the provided information."""
    if magnitude:
        magnitude = round(magnitude, 1)
        topic_name += f"-{magnitude}"
    if latitude and longitude and radius:
        latitude = location_formatting(latitude)
        longitude = location_formatting(longitude)
        topic_name += f"-{latitude}-{longitude}-{radius}"
    return topic_name


def location_formatting(coordinate: float) -> str:
    """Returns a formatted string of the latitude / longitude coordinate."""
    if coordinate < 0:
        return f"m{round(coordinate * -1, 4)}"
    return f"p{round(coordinate, 4)}"


def create_topic(sns: client, topic_name: str) -> str:
    """Creates a topic and returns the TopicARN."""
    return sns.create_topic(Name=topic_name)["TopicArn"]


def sub_to_topic(sns: client, topic_arn: str, email: str) -> None:
    """Subscribes a user to a topic based on the TopicArn."""
    sns.subscribe(TopicArn=topic_arn,
                  Protocol="email",
                  Endpoint=email)
