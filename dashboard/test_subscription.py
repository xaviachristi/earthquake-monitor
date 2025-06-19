# pylint: skip-file
"""Tests for subscription module."""

from subscription import (make_subscription,
                          create_topic_name,
                          format_coordinate)


class TestMakeSubscription:
    """Class that groups tests for make_subscription."""
    pass


class TestCreateTopicName:
    """Class that groups tests for create_topic_name."""

    def test_create_topic_name_positive(self):
        """Tests that the function returns an appropriately formatted string when given
        positive values."""
        assert create_topic_name(
            10.10, 12.5, 102, 5.4) == "c17-quake-54-p101000-p125000-102"

    def test_create_topic_name_negative(self):
        """Tests that the function returns an appropriately formatted string when given
        negative values."""
        assert create_topic_name(
            -10.10, -12.5, 102, 5.0) == "c17-quake-50-m101000-m125000-102"

    def test_create_topic_name_five_dp(self):
        """Tests that the function returns an appropriately formatted string when given
        negative values."""
        assert create_topic_name(
            -10.10123, 12.51415, 102, 5.0) == "c17-quake-50-m101012-p125142-102"


class TestFormatCoordinate:
    """Class that groups tests for format_coordinate."""

    def test_format_coordinate_positive(self):
        """Tests that the function returns an appropriately formatted string when given
        positive values."""
        assert format_coordinate(5.1234) == "p51234"

    def test_format_coordinate_negative(self):
        """Tests that the function returns an appropriately formatted string when given
        negative values."""
        assert format_coordinate(-44.8114) == "m448114"

    def test_format_coordinate_five_dp(self):
        """Tests that the function returns an appropriately formatted string when given
        extra decimal places."""
        assert format_coordinate(10.12304) == "p101230"
