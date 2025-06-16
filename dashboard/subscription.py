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
                      latitude: float, longitude: float, radius: int, magnitude: float):
    """Create a subscription to a topic for their preference.
    format: c17-quake-<magnitude>-(p/m)<latitude>-(p/m)<longitude>-<radius>"""
    topic_name = "c17-quake"

    # Format magnitude float?
    # Format lat and lon float?


def create_topic(sns: client, topic_name: str) -> str:
    """Creates a topic and returns the TopicARN."""
    return sns.create_topic(Name=topic_name)["TopicArn"]


def sub_to_topic(sns: client, topic_arn: str, email: str) -> None:
    """Subscribes a user to a topic based on the TopicArn."""
    sub = sns.subscribe(TopicArn=topic_arn,
                        Protocol="email",
                        Endpoint=email)
