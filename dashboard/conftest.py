# pylint: skip-file
"""Test fixtures for dashboard tests."""

from datetime import datetime

from pytest import fixture
from pandas import DataFrame


@fixture()
def sample_data():
    return DataFrame({
        "magnitude": [4.5, 5.0, 6.1],
        "State Name": ["California", "Nevada", "California"],
        "Region Name": ["West", "West", "West"],
        "Earthquake Count": [10, 5, 15],
        "latitude": [36.77, 38.58, 34.05],
        "longitude": [-119.42, -121.49, -118.24],
        "time": [datetime(2022, 5, 1), datetime(2022, 6, 1), datetime(2022, 7, 1)]
    })


@fixture(name="db_return")
def test_db_return():
    """Expected single record return from database for dashboard."""
    return DataFrame([
        {
            "earthquake_id": 1000001234,
            "magnitude": 6.2,
            "latitude": 35.6895,
            "longitude": 139.6917,
            "time": "2025-05-20T14:32:00Z",
            "updated": "2025-05-20T14:40:00Z",
            "depth": 10.0,
            "url": "https://earthquake.usgs.gov/earthquakes/eventpage/1000001234",
            "felt": 150,
            "tsunami": True,
            "cdi": 5.2,
            "mmi": 4.8,
            "nst": 45,
            "sig": 600,
            "net": "us",
            "dmin": 0.12,
            "alert": "orange",
            "location_source": "us",
            "magnitude_type": "Mw",
            "state_id": 12,
            "state_name": "Tokyo",
            "region_id": 3,
            "region_name": "Kanto"
        },
        {
            "earthquake_id": 1000001235,
            "magnitude": 5.5,
            "latitude": 38.2682,
            "longitude": 140.8694,
            "time": "2025-05-21T09:20:00Z",
            "updated": "2025-05-21T09:27:00Z",
            "depth": 15.0,
            "url": "https://earthquake.usgs.gov/earthquakes/eventpage/1000001235",
            "felt": 80,
            "tsunami": False,
            "cdi": 4.0,
            "mmi": 3.7,
            "nst": 35,
            "sig": 450,
            "net": "us",
            "dmin": 0.18,
            "alert": "yellow",
            "location_source": "us",
            "magnitude_type": "Mb",
            "state_id": 13,
            "state_name": "Sendai",
            "region_id": 4,
            "region_name": "Tohoku"
        },
        {
            "earthquake_id": 1000001236,
            "magnitude": 4.9,
            "latitude": 36.6513,
            "longitude": 138.1810,
            "time": "2025-05-22T03:15:00Z",
            "updated": "2025-05-22T03:20:00Z",
            "depth": 8.0,
            "url": "https://earthquake.usgs.gov/earthquakes/eventpage/1000001236",
            "felt": 60,
            "tsunami": False,
            "cdi": 3.5,
            "mmi": 2.9,
            "nst": 28,
            "sig": 300,
            "net": "us",
            "dmin": 0.10,
            "alert": "green",
            "location_source": "us",
            "magnitude_type": "Mw",
            "state_id": 14,
            "state_name": "Nagano",
            "region_id": 5,
            "region_name": "Chubu"
        },
        {
            "earthquake_id": 1000001237,
            "magnitude": 5.8,
            "latitude": 35.6895,
            "longitude": 139.6917,
            "time": "2025-05-23T11:00:00Z",
            "updated": "2025-05-23T11:05:00Z",
            "depth": 12.0,
            "url": "https://earthquake.usgs.gov/earthquakes/eventpage/1000001237",
            "felt": 100,
            "tsunami": False,
            "cdi": 4.8,
            "mmi": 4.2,
            "nst": 40,
            "sig": 520,
            "net": "us",
            "dmin": 0.14,
            "alert": "orange",
            "location_source": "us",
            "magnitude_type": "Mw",
            "state_id": 12,
            "state_name": "Tokyo",
            "region_id": 3,
            "region_name": "Kanto"
        },
        {
            "earthquake_id": 1000001238,
            "magnitude": 6.0,
            "latitude": 38.2682,
            "longitude": 140.8694,
            "time": "2025-05-24T22:45:00Z",
            "updated": "2025-05-24T22:52:00Z",
            "depth": 18.0,
            "url": "https://earthquake.usgs.gov/earthquakes/eventpage/1000001238",
            "felt": 130,
            "tsunami": True,
            "cdi": 5.0,
            "mmi": 4.5,
            "nst": 48,
            "sig": 580,
            "net": "us",
            "dmin": 0.20,
            "alert": "red",
            "location_source": "us",
            "magnitude_type": "Mw",
            "state_id": 13,
            "state_name": "Sendai",
            "region_id": 4,
            "region_name": "Tohoku"
        }
    ])


@fixture(name="query_response")
def test_query_response():
    """Expected dataframe extracted from database for dashboard."""
    return [
        {
            "earthquake_id": 1000001234,
            "magnitude": 6.2,
            "latitude": 35.6895,
            "longitude": 139.6917,
            "time": "2025-05-20T14:32:00Z",
            "updated": "2025-05-20T14:40:00Z",
            "depth": 10.0,
            "url": "https://earthquake.usgs.gov/earthquakes/eventpage/1000001234",
            "felt": 150,
            "tsunami": True,
            "cdi": 5.2,
            "mmi": 4.8,
            "nst": 45,
            "sig": 600,
            "net": "us",
            "dmin": 0.12,
            "alert": "orange",
            "location_source": "us",
            "magnitude_type": "Mw",
            "state_id": 12,
            "state_name": "Tokyo",
            "region_id": 3,
            "region_name": "Kanto"
        },
        {
            "earthquake_id": 1000001235,
            "magnitude": 5.5,
            "latitude": 38.2682,
            "longitude": 140.8694,
            "time": "2025-05-21T09:20:00Z",
            "updated": "2025-05-21T09:27:00Z",
            "depth": 15.0,
            "url": "https://earthquake.usgs.gov/earthquakes/eventpage/1000001235",
            "felt": 80,
            "tsunami": False,
            "cdi": 4.0,
            "mmi": 3.7,
            "nst": 35,
            "sig": 450,
            "net": "us",
            "dmin": 0.18,
            "alert": "yellow",
            "location_source": "us",
            "magnitude_type": "Mb",
            "state_id": 13,
            "state_name": "Sendai",
            "region_id": 4,
            "region_name": "Tohoku"
        },
        {
            "earthquake_id": 1000001236,
            "magnitude": 4.9,
            "latitude": 36.6513,
            "longitude": 138.1810,
            "time": "2025-05-22T03:15:00Z",
            "updated": "2025-05-22T03:20:00Z",
            "depth": 8.0,
            "url": "https://earthquake.usgs.gov/earthquakes/eventpage/1000001236",
            "felt": 60,
            "tsunami": False,
            "cdi": 3.5,
            "mmi": 2.9,
            "nst": 28,
            "sig": 300,
            "net": "us",
            "dmin": 0.10,
            "alert": "green",
            "location_source": "us",
            "magnitude_type": "Mw",
            "state_id": 14,
            "state_name": "Nagano",
            "region_id": 5,
            "region_name": "Chubu"
        },
        {
            "earthquake_id": 1000001237,
            "magnitude": 5.8,
            "latitude": 35.6895,
            "longitude": 139.6917,
            "time": "2025-05-23T11:00:00Z",
            "updated": "2025-05-23T11:05:00Z",
            "depth": 12.0,
            "url": "https://earthquake.usgs.gov/earthquakes/eventpage/1000001237",
            "felt": 100,
            "tsunami": False,
            "cdi": 4.8,
            "mmi": 4.2,
            "nst": 40,
            "sig": 520,
            "net": "us",
            "dmin": 0.14,
            "alert": "orange",
            "location_source": "us",
            "magnitude_type": "Mw",
            "state_id": 12,
            "state_name": "Tokyo",
            "region_id": 3,
            "region_name": "Kanto"
        },
        {
            "earthquake_id": 1000001238,
            "magnitude": 6.0,
            "latitude": 38.2682,
            "longitude": 140.8694,
            "time": "2025-05-24T22:45:00Z",
            "updated": "2025-05-24T22:52:00Z",
            "depth": 18.0,
            "url": "https://earthquake.usgs.gov/earthquakes/eventpage/1000001238",
            "felt": 130,
            "tsunami": True,
            "cdi": 5.0,
            "mmi": 4.5,
            "nst": 48,
            "sig": 580,
            "net": "us",
            "dmin": 0.20,
            "alert": "red",
            "location_source": "us",
            "magnitude_type": "Mw",
            "state_id": 13,
            "state_name": "Sendai",
            "region_id": 4,
            "region_name": "Tohoku"
        }
    ]


@fixture(name="state_counts")
def test_state_counts():
    """Expected region counts."""
    return DataFrame.from_dict({
        "State Name": ["Tokyo", "Sendai", "Nagano"],
        "Earthquake Count": [2, 2, 1]
    })
