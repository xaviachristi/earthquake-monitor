"""Module that creates and formats the notification messages."""

import logging
from datetime import datetime
from os import environ as ENV

from dotenv import load_dotenv
from boto3 import client
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

logging.basicConfig(
    level="DEBUG",
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S"
)


def get_sns_client() -> client:
    """Makes a SNS client."""
    sns = client("sns", aws_access_key_id=ENV["ACCESS_KEY"],
                 aws_secret_access_key=ENV["SECRET_ACCESS_KEY"])
    return sns


def validate_keys(data: dict) -> bool:
    """Checks all the required keys are in the dictionary."""
    keys = ["topic_arn", "magnitude", "state_name", "region_name", "time",
            "tsunami", "latitude", "longitude"]
    logger.info("Starting key validation for topic %s.", data.get("topic_arn"))
    for key in keys:
        if key not in data:
            logger.error("Unable to validate %s key in data:\n %s", key, data)
            return False
    return True


def validate_types(data: dict) -> bool:
    """Validates that the required information for a message is available."""
    expected_data = [("topic_arn", str), ("magnitude", float), ("state_name", str),
                     ("region_name", str), ("time", str), ("tsunami", bool),
                     ("latitude", float), ("longitude", float)]
    logger.info("Starting datatype validation for topic %s.",
                data["topic_arn"])
    for name, expected_type in expected_data:
        if not isinstance(data[name], expected_type):
            logger.error(
                "Unable to validate %s datatype for the %s key in data:\n %s",
                expected_type, name, data)
            return False
    return True


def get_location_message(data: dict) -> str:
    """Returns a string for the location depending on if
    it is within the USA or not."""
    if data["state_name"] == "Not in the USA":
        return data["region_name"]
    return f"the area of {data["state_name"]}, {data["region_name"]}"


def make_message(data: dict) -> str:
    """Turns a dictionary of values into a string 
    that makes up the alert message."""
    logger.info("Starting message creation for topic %s.", data["topic_arn"])
    time = data["time"]
    heading = "------ Earthquake Alert! ------\n"
    body = f"\nThere was an earthquake of magnitude {data["magnitude"]} in"
    body += f" {get_location_message(data)} at {time}.\n"
    if data["tsunami"]:
        body += "There is potential for a tsunami.\n"
    body += f"Precise latitude and longitude location of earthquake:\n"
    body += f"  ({data["latitude"]}, {data["longitude"]})."
    return heading+body


def publish_email(data: dict, sns: client) -> None:
    """Sends the email to SNS."""
    logger.info("Starting email publication for topic %s.", data["topic_arn"])
    try:
        message = make_message(data)
        topic = data["topic_arn"]
        subject = "Earthquake Alert"
        response = sns.publish(
            TopicArn=topic, Subject=subject, Message=message)
        message_id = response["MessageId"]
        logger.info("Published message %s to topic %s.",
                    message_id, topic)
    except ClientError:
        logger.exception("Couldn't publish message to topic %s.", topic)
        raise


def send_emails(passed_data: list[dict], sns: client) -> None:
    """Goes through all the topics generated."""
    for data in passed_data:
        if validate_keys(data) and validate_types(data):
            publish_email(data, sns)
    logger.info("Successfully sent all emails.")
