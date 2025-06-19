# pylint: skip-file

"""Unit tests for the functions in extract.py."""

from datetime import datetime, timedelta
import asyncio

from unittest.mock import patch

from extract import (get_event_ids_from_json_list, create_usgs_urls_from_event_ids,
                     make_many_api_calls, extract)


class TestGetEventIDsFromJSONList:

    def test_get_event_ids_from_json_list_two_items(self):
        example_event_list = [{"id": "A1",}, {"id": "L2"}]
        assert get_event_ids_from_json_list(example_event_list) == ["A1", "L2"]

    def test_get_event_ids_from_json_list_three_items(self):
        example_event_list = [{"id": "gv123 hb", "other cat.":"data"}, {"id": "L2"}, {"id":"id"}]
        assert get_event_ids_from_json_list(example_event_list) == [
            "gv123 hb", "L2", "id"]
        
    def test_get_event_ids_from_json_list_no_items(self):
        example_event_list = []
        assert get_event_ids_from_json_list(example_event_list) == []


class TestCreateUSGSUrlsFromEventIDs:

    def test_create_usgs_urls_from_event_ids_one_id(self):
        event_ids = ["test_id"]
        assert create_usgs_urls_from_event_ids(
            event_ids) == ["https://earthquake.usgs.gov/earthquakes/feed/v1.0/detail/test_id.geojson"]

    def test_create_usgs_urls_from_event_ids_two_ids(self):
        event_ids = ["tx2025lmnxxe", "us6000qjtq"]
        assert create_usgs_urls_from_event_ids(
            event_ids) == ["https://earthquake.usgs.gov/earthquakes/feed/v1.0/detail/tx2025lmnxxe.geojson", "https://earthquake.usgs.gov/earthquakes/feed/v1.0/detail/us6000qjtq.geojson"]
    
    def test_create_usgs_urls_from_event_ids_no_ids(self):
        event_ids = []
        assert create_usgs_urls_from_event_ids(
            event_ids) == []

    def test_create_usgs_urls_from_event_ids_many_ids(self, event_ids, event_urls):
        assert create_usgs_urls_from_event_ids(
            event_ids) == event_urls


@patch("extract.make_api_call")
class TestMakeManyAPICalls:

    def test_make_many_api_calls(self, make_api_call, example_earthquake_api_response, event_urls):
        make_api_call.response_content = {"Api Call Made":True}
        assert len(asyncio.run(make_many_api_calls(event_urls))) == len(event_urls)


@patch("extract.access_api")
class TestExtract:

    def test_extract_1(self, access_api, example_earthquake_api_response):
        access_api.response_content = example_earthquake_api_response
        assert isinstance(extract("USGS",
            datetime.now() - timedelta(days=1), datetime.now()
            ), list)
