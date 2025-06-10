"""Unit tests for the functions in extract.py."""

from extract import convert_catalog_to_dataframe

import pandas as pd
import obspy


class TestConvertCatalogToDataFrame:

    def test_convert_catalog_to_dataframe_returns_dataframe(self):
        test_cat = obspy.core.event.catalog._create_example_catalog()
        assert isinstance(convert_catalog_to_dataframe(test_cat), pd.DataFrame)

    def test_convert_catalog_to_dataframe_returns_dataframe_with_correct_data(self):
        pass

    def test_convert_catalog_to_dataframe_returns_dataframe_with_correct_data(self):
        pass
