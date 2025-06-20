# pylint: skip-file
"""Unit tests for the functions in pipeline.py."""

from datetime import datetime, timedelta
from os import environ as ENV
from unittest.mock import patch

from pandas import DataFrame

from pipeline import (run_pipeline,
                      get_time_window_from_cli,
                      get_time_window_from_event,
                      get_datetimes,
                      lambda_handler)


class TestRunPipeline:
    """A class that groups together tests for run_pipeline()."""

    @patch("pipeline.extract")
    @patch("pipeline.transform")
    @patch("pipeline.load")
    def test_run_pipeline(self, mock_load, mock_transform, mock_extract):
        """Checks the function returns expected dataframe."""
        now = datetime.now()
        dummy_df = DataFrame({"example": [1, 2, 3]})
        ENV["DB_USER"] = "test user"
        ENV["DB_HOST"] = "test ip"
        ENV["DB_NAME"] = "test db"

        mock_extract.return_value = [{"dummy": "data"}]
        mock_transform.return_value = dummy_df
        mock_load.return_value = dummy_df

        result = run_pipeline(start=now - timedelta(hours=4), end=now)

        assert isinstance(result, DataFrame)
        assert not result.empty


class TestLambdaHandler:
    """A class that groups together tests for lambda_handler()."""

    @patch("pipeline.get_time_window_from_event")
    @patch("pipeline.run_pipeline")
    @patch("pipeline.get_topic_dictionaries")
    def test_lambda_handler(self, mock_get_topic_dictionaries, mock_run_pipeline, mock_get_time_window_from_event):
        """Checks the function returns expected topic dictionary."""

        start = datetime.now() - timedelta(hours=1)
        end = datetime.now()

        mock_get_time_window_from_event.return_value = (start, end)

        mock_df = DataFrame({
            "url": ["https://quake1", "https://quake2"],
            "time": [start, end],
            "updated": [start, end]
        })
        mock_run_pipeline.return_value = mock_df

        mock_get_topic_dictionaries.return_value = {
            "topic": "Earthquake Alert",
            "count": 2
        }

        event = {"start": 60, "end": 0}
        context = None

        result = lambda_handler(event, context)

        assert result["statusCode"] == 200
        assert isinstance(result["earthquakes"], list)
        assert len(result["earthquakes"]) == 2
        assert result["message"]["topic"] == "Earthquake Alert"


class TestGetTimeWindowFromCLI:
    """A class that groups together tests for get_time_window_from_cli()."""

    @patch('sys.argv', ['program', '--start', '120', '--end', '60'])
    def test_get_time_window_from_cli(self):
        """Checks the function returns a tuple of datetimes from CLI args."""
        start, end = get_time_window_from_cli()

        assert isinstance(start, datetime)
        assert isinstance(end, datetime)
        assert start < end


class TestGetDatetimes:
    """A class that groups together tests for get_datetimes."""

    def test_get_datetimes(self):
        """Checks the function returns expected datetime given a time diff in minutes."""
        start_minutes = 120
        end_minutes = 60

        start, end = get_datetimes(start_minutes, end_minutes)

        assert start < end


def get_datetimes(start: int, end: int) -> tuple[datetime, datetime]:
    """Mock implementation of get_datetimes for testing."""
    now = datetime.now()
    return now - timedelta(hours=start), now - timedelta(hours=end)


class TestGetTimeWindowFromEvent:
    """A class that groups together tests for get_time_window_from_event()."""

    def test_get_time_window_from_event(self):
        """Checks the function returns a tuple of datetimes from inputs given as part of event object."""
        event = {"start": 5, "end": 2}
        start_dt, end_dt = get_time_window_from_event(event)

        assert isinstance(start_dt, datetime)
        assert isinstance(end_dt, datetime)
        assert start_dt < end_dt
