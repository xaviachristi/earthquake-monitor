"""Unit tests for the functions in extract.py."""

from transform import make_row_for_dataframe, is_event_clean

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


class TestIsEventClean:
    
    def test_is_event_clean_pos_1(self):
        clean_event = {"properties":{"type":"earthquake", "ids": "test_earthquake_id"}}
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
    pass


class TestGetAddress:
    pass


class TestGrabState:
    pass


class TestGetRegionFromState:
    pass


class TestMakeRowForDataFrame:
    pass


class TestCreateDataFrameExpectedForLoad:
    pass


class TestTransform:
    pass
