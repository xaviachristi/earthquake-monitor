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


@fixture
def example_df():
    """Example dataframe with two earthquake entries."""
    return DataFrame([
        {
            "earthquake_id": 1, "magnitude": 2.5, "latitude": 10.0, "longitude": 20.0,
            "time": "2024-01-01", "updated": "2024-01-02", "depth": 5.0, "url": "example.com",
            "felt": 1, "tsunami": 0, "cdi": 3.1, "mmi": 2.3, "nst": 1,
            "sig": 1, "net": "us", "dmin": 0.1, "alert": "green",
            "location_source": "us", "magnitude_type": "mb",
            "state_name": "California", "region_name": "West Coast",
            "state_id": 12, "region_id": 4
        },
        {
            "earthquake_id": 2, "magnitude": 4.0, "latitude": 11.0, "longitude": 21.0,
            "time": "2024-02-01", "updated": "2024-02-02", "depth": 10.0, "url": "another.com",
            "felt": 2, "tsunami": 1, "cdi": 3.0, "mmi": 2.5, "nst": 5,
            "sig": 100, "net": "us", "dmin": 0.1, "alert": "green",
            "location_source": "us", "magnitude_type": "mb",
            "state_name": "Nevada", "region_name": "West Coast",
            "state_id": 13, "region_id": 4
        }
    ])


@fixture
def example_df2():
    """Second example dataframe with one duplicate entry from example_df."""
    return DataFrame([
        {
            "earthquake_id": 1, "magnitude": 2.5, "latitude": 10.0, "longitude": 20.0,
            "time": "2024-01-01", "updated": "2024-01-02", "depth": 5.0, "url": "example.com",
            "felt": 1, "tsunami": 0, "cdi": 3.1, "mmi": 2.3, "nst": 1,
            "sig": 1, "net": "us", "dmin": 0.1, "alert": "green",
            "location_source": "us", "magnitude_type": "mb",
            "state_name": "California", "region_name": "West Coast"
        }
    ])


@fixture
def example_diff():
    """Expected difference between example_df and example_df2 (only the unique row)."""
    return DataFrame([
        {
            "magnitude": 4.0, "latitude": 11.0, "longitude": 21.0,
            "time": "2024-02-01", "updated": "2024-02-02", "depth": 10.0, "url": "another.com",
            "felt": 2, "tsunami": 1, "cdi": 3.0, "mmi": 2.5, "nst": 5,
            "sig": 100, "net": "us", "dmin": 0.1, "alert": "green",
            "location_source": "us", "magnitude_type": "mb",
            "state_name": "Nevada", "region_name": "West Coast"
        }
    ])
