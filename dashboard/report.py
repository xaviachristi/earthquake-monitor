"""Module for handling summary reports."""

from datetime import date, datetime
from os import environ as ENV

from boto3 import client
from streamlit import cache_resource


def get_client() -> client:
    """Return client for S3."""
    return client("s3")


@cache_resource
def get_report(target: date = None) -> bytes:
    """Return report from S3 for given date as bytes."""
    s3 = get_client()
    files = s3.list_objects(Bucket=ENV["AWS_S3_BUCKET"]).get('Contents')
    for file in files:
        key = file.get("Key")
        if key:
            file_date_string = key.split("_")[2].rstrip(".pdf")
            file_date = datetime.strptime(file_date_string, r"%Y-%m-%d")
            if file_date.date() == target:
                streaming_body = s3.get_object(Bucket=ENV["AWS_S3_BUCKET"],
                                               Key=key).get('Body')
                return streaming_body.read()
    return b""
