# pylint: skip-file
"""Unit tests for the functions in load.py."""

from unittest.mock import MagicMock, call, patch

from pandas import DataFrame
from pandas.testing import assert_frame_equal

from load import (get_current_db, get_diff, upload_df_to_db)


class TestGetCurrentDB:
    """A class that groups together tests for get_current_db()."""

    def test_get_current_db_returns_dataframe(self, mock_conn, example_dict):
        """Checks the function returns a dataframe."""
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [example_dict]
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

        df = get_current_db(mock_conn)
        assert isinstance(df, DataFrame)

    def test_get_current_db_returns_expected_columns(self, mock_conn, example_dict):
        """Checks the function has all expected columns."""
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [example_dict]
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

        df = get_current_db(mock_conn)
        expected_cols = {
            "earthquake_id", "magnitude", "latitude", "longitude", "time", "updated", "depth",
            "url", "felt", "tsunami", "cdi", "mmi", "nst", "sig", "net", "dmin",
            "alert", "location_source", "magnitude_type", "state_name", "region_name"
        }
        assert set(df.columns) == expected_cols


class TestGetDiff:
    """A class that groups together tests for get_diff()."""

    def test_get_diff_returns_dataframe(self, example_df, example_df2):
        """Checks the function returns a dataframe."""
        diff_df = get_diff(example_df, example_df2)
        assert isinstance(diff_df, DataFrame)

    def test_get_diff_returns_expected_diff(self, example_df, example_df2, example_diff):
        """Checks the function returns expected difference between two dataframes."""
        diff_df = get_diff(example_df, example_df2)
        assert_frame_equal(diff_df.reset_index(drop=True),
                           example_diff.reset_index(drop=True))


class TestUploadDFToDB:
    """A class that groups together tests for upload_df_to_db."""

    def test_get_upload_df_to_db_expected_calls(self, example_df):
        """Check that upload_df_to_db has expected calls to upload_row_to_db."""
        mock_conn = MagicMock()

        with patch("load.upload_row_to_db") as mock_upload:
            mock_upload.return_value = None
            upload_df_to_db(mock_conn, example_df)
            assert mock_upload.call_count == len(example_df)
            for _, row in example_df.iterrows():
                mock_upload.assert_any_call(mock_conn, row.to_dict())
