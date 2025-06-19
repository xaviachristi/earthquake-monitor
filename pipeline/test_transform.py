# pylint: skip-file

"""Unit tests for the functions in extract.py."""

from transform import (is_event_clean, make_row_for_dataframe, clean_earthquake_data,
                       grab_state, get_region_from_state, create_dataframe_expected_for_load)


class TestIsEventClean:

    def test_is_event_clean_pos_1(self):
        clean_event = {"properties": {
            "type": "earthquake", "ids": "test_earthquake_id"}}
        assert is_event_clean(clean_event)

    def test_is_event_clean_pos_2(self):
        clean_event = {"properties": {"type": "earthquake",
                                      "ids": "test_earthquake_id", "mag": "2.4"}}
        assert is_event_clean(clean_event)

    def test_is_event_clean_neg_1(self):
        unclean_event = {"properties": {"type": "not an earthquake",
                                        "ids": ["test_earthquake_id"], "mag": "2.4"}}
        assert not is_event_clean(unclean_event)

    def test_is_event_clean_neg_2(self):
        unclean_event = {"properties": {"type": "quarry",
                                        "ids": ["test_earthquake_id"]}}
        assert not is_event_clean(unclean_event)

    def test_is_event_clean_neg_3(self):
        unclean_event = {"prerties": {"type": "quarry",
                                      "ids": ["test_earthquake_id"]}}
        assert not is_event_clean(unclean_event)

    def test_is_event_clean_neg_4(self):
        unclean_event = {}
        assert not is_event_clean(unclean_event)


class TestCleanEarthquakeData:

    def test_clean_earthquake_data_two_clean(self,
                                             earthquake_data_with_unclean_events,
                                             earthquake_data_with_unclean_events_cleaned):
        assert clean_earthquake_data(
            earthquake_data_with_unclean_events
            ) == earthquake_data_with_unclean_events_cleaned
    
    def test_clean_earthquake_data_none(self):
        assert clean_earthquake_data([]) == []


class TestGrabState:
    
    def test_grab_state_with_zip_code(self):
        assert grab_state(
            ["15 Fish Place", "56 East", "Springfield", "Illinois", "79842", "United States"]
            ) == "Illinois"
        
    def test_grab_state_without_a_zip_code(self):
        assert grab_state(
            ["15 Fish Place", "56 East", "Springfield",
                "Illinois", "United States"]
        ) == "Illinois"


class TestGetRegionFromState:
    
    def test_get_region_from_state_nevada(self):
        assert get_region_from_state("nevada") == "Southwest"

    def test_get_region_from_state_north_dakota(self):
        assert get_region_from_state("noRth dakoTa") == "Midwest"
    
    def test_get_region_from_state_pr(self):
        assert get_region_from_state(
            "Puerto Rico") == "Puerto Rico"

    def test_get_region_from_state_no_state(self):
        assert get_region_from_state(
            "unknown state") == "Unspecified United States"


class TestMakeRowForDataFrame:

    def test_make_row_for_dataframe(self, example_detailed_event):
        """Example test for make_row_from_dataframe()."""
        desired_output = [['ci41182664'], 0.53, '33.6663333', '-116.771',
                          1749655031680, 1749675581157, '15.81',
                          'https://earthquake.usgs.gov/earthquakes/eventpage/ci41182664',
                          None, 0, None, None, 15, 4, 'ci', 0.06854, None, [
            'ci'], 'ml',
            'Not in the USA', 'No Country']
        assert make_row_for_dataframe(example_detailed_event) == desired_output


class TestCreateDataFrameExpectedForLoad:

    def test_create_dataframe_expected_for_load_has_earthquake_id(self):
        assert "earthquake_id" in create_dataframe_expected_for_load().columns

    def test_create_dataframe_expected_for_load_has_magnitude(self):
        assert "magnitude" in create_dataframe_expected_for_load().columns

    def test_create_dataframe_expected_for_load_has_all_correct_columns(self):
        assert {"earthquake_id", "magnitude", "latitude",
                   "longitude", "time", "updated", "depth", "url",
                   "felt", "tsunami", "cdi", "mmi", "nst", "sig",
                   "net", "dmin", "alert", "location_source",
                   "magnitude_type", "state_name", "region_name"
                }.issubset(create_dataframe_expected_for_load().columns)
