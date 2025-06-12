"""Module that creates and formats the notification messages."""

import logging
from datetime import datetime

from boto3 import client

logger = logging.getLogger(__name__)

logging.basicConfig(
    level="DEBUG",
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S"
)


def get_sns_client() -> client:
    sns = client("sns")
    return sns


def validate_topic(data: dict) -> bool:
    """Validates that the data contains a topic key."""
    if data.get("topic") and len(data["topic"]) > 1:
        return True
    return False


def validate_magnitude(data: dict) -> bool:
    """Validates that the data contains a magnitude key."""
    if data.get("magnitude") and isinstance(data["magnitude"], float):
        return True
    return False


def validate_state(data: dict) -> bool:
    """Validates that the data contains a state key."""
    if data.get("state_name") and isinstance(data["state_name"], str):
        return True
    return False


def validate_region(data: dict) -> bool:
    """Validates that the data contains a region key."""
    if data.get("region_name") and isinstance(data["region_name"], str):
        return True
    return False


def validate_time(data: dict) -> bool:
    """Validates that the data contains a time key."""
    if data.get("time") and isinstance(data["time"], datetime):
        return True
    return False


def validate_tsunami(data: dict) -> bool:
    """Validates that the data contains a tsunami key."""
    if data.get("tsunami") and isinstance(data["tsunami"], bool):
        return True
    return False


def validate_latitude(data: dict) -> bool:
    """Validates that the data contains a latitude key."""
    if data.get("latitude") and isinstance(data["latitude"], float):
        return True
    return False


def validate_longitude(data: dict) -> bool:
    """Validates that the data contains a longitude key."""
    if data.get("longitude") and isinstance(data["longitude"], str):
        return True
    return False


def validate_data(data: dict) -> bool:
    """Validates that the required information for a message is available."""
    ...


def make_message(data: dict) -> str:
    """Turns a dictionary of values into a string 
    of HTML that makes up the alert message."""
    heading = """<!DOCTYPE html>
                 <html>
                 <body>
                 <h1> Earthquake Alert! </h1>"""
    body = f"""<p> There was an earthquake of magnitude {data["magnitude"]} in
    the area of {data["state_name"]} in the region of {data["region_name"]} at {data["time"]}. </p>
    """

    if data["tsunami"]:
        body += """<p> There is potential for a tsunami. </p>"""

    body += f"""<p> Precise latitude and longitude location of earthquake:
      ({data["latitude"]}, {data["longitude"]}). </p>
      </body>
      </html>
      """
    return heading+body


def publish_email(data: dict, sns: client) -> None:
    """Sends the email to SNS."""
    try:
        message = make_message(data)
        topic = data["topic"]
        subject = "Earthquake Alert"
        response = sns.publish(
            TopicArn=topic, Subject=subject, Message=message)
        message_id = response["MessageId"]
        logger.info("Published message %s to topic %s.",
                    message_id, topic)
    except sns.ClientError:
        logger.exception("Couldn't publish message to topic %s.", topic)
