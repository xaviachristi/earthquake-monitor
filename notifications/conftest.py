# pylint: skip-file

from datetime import datetime

from pytest import fixture


@fixture(name="sample_data")
def get_sample_data():
    """Expected data passed to notification maker."""
    data = {"topic_arn": "a", "magnitude": 3.1, "state_name": "state", "region_name": "region",
            "time": "2025/12/13 13:40", "tsunami": False, "latitude": 30.101, "longitude": 50.123}
    return data


@fixture(name="sample_non_usa_data")
def get_sample_non_usa_data():
    """Expected data passed to notification maker
    when an earthquake outside of the USA is detected."""
    data = {"topic_arn": "a", "magnitude": 3.1, "state_name": "Not in the USA", "region_name": "Taiwan",
            "time": "2025/12/13 13:40", "tsunami": False, "latitude": 30.101, "longitude": 50.123}
    return data
