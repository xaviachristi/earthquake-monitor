"""Unit tests for the functions in extract.py."""

from transform import make_row_for_dataframe


def test_make_row_for_dataframe(example_detailed_event):
    """Example test for make_row_from_dataframe()."""
    desired_output = [['ci41182664'], 0.53, '33.6663333', '-116.771',
                      1749655031680, 1749675581157, '15.81',
                      'https://earthquake.usgs.gov/earthquakes/eventpage/ci41182664',
                      None, 0, None, None, 15, 4, 'ci', 0.06854, None, [
                          'ci'], 'ml',
                      'Not in the USA', 'No Country']
    assert make_row_for_dataframe(example_detailed_event) == desired_output
