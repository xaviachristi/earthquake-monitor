"""Unit tests for the functions in extract.py."""

from extract import convert_catalog_to_dataframe

import pandas as pd


class TestConvertCatalogToDataFrame:

    def test_convert_catalog_to_dataframe_returns_dataframe(self, example_catalog):
        """Checks the function returns a dataframe."""
        assert isinstance(convert_catalog_to_dataframe(
            example_catalog), pd.DataFrame)

    def test_convert_catalog_to_dataframe_has_magnitudes_column(self, example_catalog):
        """Checks the function has a 'magnitudes' column."""
        assert "magnitudes" in convert_catalog_to_dataframe(
            example_catalog).columns

    def test_convert_catalog_to_dataframe_has_event_type_column(self, example_catalog):
        """Checks the function has an 'event_type' column."""
        assert "event_type" in convert_catalog_to_dataframe(
            example_catalog).columns

    def test_convert_catalog_to_dataframe_has_origins_column(self, example_catalog):
        """Checks the function has an 'origins' column."""
        assert "origins" in convert_catalog_to_dataframe(
            example_catalog).columns
