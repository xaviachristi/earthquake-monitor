"""Unit tests for the functions in load.py."""

from unittest.mock import MagicMock, call

from pandas import DataFrame
from pandas.testing import assert_frame_equal

from load import (get_current_db, get_diff, upload_df_to_db)


class TestGetCurrentDB:
    """A class that groups together tests for get_current_db()."""

    def test_get_current_db_returns_dataframe(self, example_dict):
        """Checks the function returns a dataframe."""

    def test_get_current_db_returns_expected_columns(self, example_dict):
        """Checks the function has a all expected column."""


class TestGetDiff:
    """A class that groups together tests for get_diff()."""

    def test_get_diff_returns_dataframe(self, example_df, example_df2):
        """Checks the function returns a dataframe."""

    def test_get_diff_returns_expected_diff(self, example_df, example_df2):
        """Checks the function returns expected difference between two dataframes."""


class TestUploadDFToDB:
    """A class that groups together tests for upload_df_to_db."""

    def test_get_upload_df_to_db_expected_calls(self, example_df):
        """Check that upload_df_to_db has expected calls to upload row to db."""
