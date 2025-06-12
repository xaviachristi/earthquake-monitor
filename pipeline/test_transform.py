"""Unit tests for the functions in extract.py."""

from transform import make_row_for_dataframe


def test_make_row_for_dataframe(example_detailed_event):
    print(make_row_for_dataframe(example_detailed_event))
    assert False
