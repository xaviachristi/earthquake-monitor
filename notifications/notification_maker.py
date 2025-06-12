"""Module that creates and formats the notification messages."""

import logging
from datetime import datetime
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
    sns = client("sns", aws_access_key_id=ENV["AWS_ACCESS_KEY"],
                 aws_secret_access_key=ENV["AWS_SECRET_ACCESS_KEY"])
    return sns


def validate_keys(data: dict) -> bool:
    """Checks all the required keys are in the dictionary."""
    keys = ["topic_arn", "magnitude", "state_name", "region_name", "time",
            "tsunami", "latitude", "longitude"]
    for key in keys:
        if key not in data:
            # TODO: Add log
            return False
    return True


def validate_types(data: dict) -> bool:
    """Validates that the required information for a message is available."""
    expected_data = [("topic_arn", str), ("magnitude", float), ("state_name", str), ("region_name", str),
                     ("time", datetime), ("tsunami", bool), ("latitude", float), ("longitude", float)]
    for name, expected_type in expected_data:
        if not isinstance(data[name], expected_type):
            # TODO: Add log
            return False
    return True


def make_message(data: dict) -> str:
    """Turns a dictionary of values into a string 
    of HTML that makes up the alert message."""
    heading = """<!DOCTYPE html>
                 <html>
                 <body>
                 <h1>Earthquake Alert!</h1>"""
    body = f"""<p>There was an earthquake of magnitude {data["magnitude"]} in
    the area of {data["state_name"]} in the region of {data["region_name"]} at {data["time"]}.</p>
    """
    if data["tsunami"]:
        body += """<p>There is potential for a tsunami.</p>"""
    body += f"""<p>Precise latitude and longitude location of earthquake:
      ({data["latitude"]}, {data["longitude"]}).</p>
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


def send_emails(passed_data: dict) -> None:
    """Goes through all the topics generated."""
    sns_client = get_sns_client()
    for data in passed_data["topics"]:
        if not validate_keys(data):
            # TODO: Add logging
            ...
        elif not validate_types(data):
            # TODO: Add logging
            ...
        else:
            publish_email(data, sns_client)
