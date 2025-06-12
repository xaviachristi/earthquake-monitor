"""File that tests the notification-making functions."""


from notification_maker import (validate_keys, validate_types,
                                make_message, get_location_message)


class TestValidateKeys:
    """A class that groups together tests for validate_keys."""
    ...


class TestValidateTypes:
    """A class that groups together tests for validate_types."""

    def test_validate_types_valid(self, sample_data, sample_non_usa_data):
        """Checks that the function returns True if all datatypes are valid."""
        assert validate_types(sample_data)
        assert validate_types(sample_non_usa_data)

    def test_validate_types_topic_invalid(self, sample_data, sample_non_usa_data):
        """Checks that the function returns False if the topic arn isn't
        of the correct datatype."""
        sample_data["topic_arn"] = 1
        sample_non_usa_data["topic_arn"] = 2
        assert not validate_types(sample_data)
        assert not validate_types(sample_non_usa_data)

    def test_validate_types_magnitude_invalid(self, sample_data, sample_non_usa_data):
        """Checks that the function returns False if the magnitude isn't
        of the correct datatype."""
        sample_data["magnitude"] = 1
        sample_non_usa_data["magnitude"] = 2
        assert not validate_types(sample_data)
        assert not validate_types(sample_non_usa_data)

    def test_validate_types_state_invalid(self, sample_data, sample_non_usa_data):
        """Checks that the function returns False if the state isn't
        of the correct datatype."""
        sample_data["state_name"] = 1
        sample_non_usa_data["state_name"] = 2
        assert not validate_types(sample_data)
        assert not validate_types(sample_non_usa_data)


class TestMakeMessage:
    """A class that groups together tests for make_message."""
    ...


class TestGetLocationMessage:
    """A class that groups together tests for get_location_message."""

    def test_get_location_message_usa(self, sample_data):
        """Checks function returns expected data for earthquakes
        occurring within the USA."""
        result = get_location_message(sample_data)
        assert result == f"the area of {sample_data["state_name"]}, {sample_data["region_name"]}"

    def test_get_location_message_non_usa(self, sample_non_usa_data):
        """Checks function returns expected data for earthquakes
        occurring outside the USA."""
        result = get_location_message(sample_non_usa_data)
        assert result == sample_non_usa_data["region_name"]
