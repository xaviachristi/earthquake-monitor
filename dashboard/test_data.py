# pylint: skip-file
"""Tests for data module."""

from unittest.mock import MagicMock, patch
from pandas import DataFrame
from pandas.testing import assert_frame_equal

from data import get_counts_by_state, get_data


class TestGetCountsByState:
    """Class that groups tests for get_count_by_state."""

    def test_get_count_by_state_returns_dataframe(self, db_return):
        """Checks function returns expected datatype."""
        result = get_counts_by_state(db_return)
        assert isinstance(result, DataFrame)

    def test_get_count_by_state_has_expected_columns(self, db_return):
        """Checks function returns expected columns."""
        result = get_counts_by_state(db_return)
        assert list(result.columns) == ["State Name", "Earthquake Count"]

    def test_get_count_by_state_returns_correct_count(self, db_return, state_counts):
        """Checks function returns correct count for each state."""
        result = get_counts_by_state(db_return)
        assert_frame_equal(result, state_counts)


class TestGetData:
    """Class that groups tests for get_data."""

    def test_get_data_returns_dataframe(query_response):
        """Checks function returns dataframe."""
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchall.return_value = query_response
        mock_cursor.execute.return_value = None
        with patch("data.get_connection", mock_connection):
            result = get_data()
        assert isinstance(result, DataFrame)
