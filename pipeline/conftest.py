"""Fixtures for tests in this directory."""

from unittest.mock import MagicMock

from pytest import fixture
from pandas import DataFrame
import obspy


@fixture
def example_catalog():
    """An example catalog for use with the ObsPy library."""
    return obspy.core.event.catalog._create_example_catalog()


@fixture
def expected_columns():
    """List of columns expected from sql query to database."""
    return [
        "earthquake_id", "magnitude", "time", "updated", "longitude", "latitude",
        "depth", "url", "tsunami", "felt", "cdi", "mmi", "nst",
        "sig", "net", "dmin", "alert", "location_source",
        "magnitude_type", "state_name", "region_name"
    ]


@fixture
def mock_conn():
    """Empty connection object."""
    return MagicMock()


@fixture
def example_dict():
    """Example record in database."""
    return {
        "earthquake_id": 1, "magnitude": 2.5, "latitude": 10.0, "longitude": 20.0,
        "time": "2024-01-01", "updated": "2024-01-02", "depth": 5.0, "url": "example.com",
        "felt": 1, "tsunami": 0, "cdi": None, "mmi": None, "nst": None,
        "sig": None, "net": None, "dmin": None, "alert": None,
        "location_source": None, "magnitude_type": None,
        "state_name": "California", "region_name": "West Coast",
        "state_id": 12, "region_id": 4
    }
