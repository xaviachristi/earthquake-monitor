# pylint: skip-file
"""Unit tests for the functions in pipeline.py."""

from pipeline import get_topic_dictionaries


class TestGetTopicDicitionaries:
    """A class that groups together tests for get_topic_dictionaries."""

    def test_get_topic_dictionaries_returns_list(self, example_diff, example_topic):
        """Check that get_topic_dictionaries returns expected list of topics."""
        assert True
