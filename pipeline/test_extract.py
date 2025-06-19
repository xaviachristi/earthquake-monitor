"""Unit tests for the functions in extract.py."""

"""
As extract.py has been modified extensively, the test ticket
should be reopened and these tests either modified or removed.
"""

# class TestConvertCatalogToDataFrame:
#     """A class that groups together tests for convert_catalog_to_dataframe()."""

#     def test_convert_catalog_to_dataframe_returns_dataframe(self, example_catalog):
#         """Checks the function returns a dataframe."""
#         assert isinstance(convert_catalog_to_dataframe(
#             example_catalog), pd.DataFrame)

#     def test_convert_catalog_to_dataframe_has_magnitudes_column(self, example_catalog):
#         """Checks the function has a 'magnitudes' column."""
#         assert "magnitudes" in convert_catalog_to_dataframe(
#             example_catalog).columns

#     def test_convert_catalog_to_dataframe_has_event_type_column(self, example_catalog):
#         """Checks the function has an 'event_type' column."""
#         assert "event_type" in convert_catalog_to_dataframe(
#             example_catalog).columns

#     def test_convert_catalog_to_dataframe_has_origins_column(self, example_catalog):
#         """Checks the function has an 'origins' column."""
#         assert "origins" in convert_catalog_to_dataframe(
#             example_catalog).columns
from datetime import datetime, timedelta

from unittest.mock import patch

from extract import extract


class TestAccessAPI:
    pass


class TestGetEventIDsFromJSONList:
    pass


class TestCreateUSGSUrlsFromEventIDs:
    pass


class TestMakeAPICall:
    pass


class TestMakeManyAPICalls:
    pass


@patch("extract.access_api")
class TestExtract:

    def test_extract_1(self, access_api, example_earthquake_api_response):
        access_api.response_content = example_earthquake_api_response
        assert isinstance(extract("USGS",
            datetime.now() - timedelta(days=1), datetime.now()
            ), list)
