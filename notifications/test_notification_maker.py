"""File that tests the notification-making functions."""


from notification_maker import (validate_keys, validate_types,
                                make_message, get_location_message)


class TestValidateKeys:
    """A class that groups together tests for validate_keys."""

    def test_validate_keys_valid(self, sample_data, sample_non_usa_data):
        """Checks that the function returns True if all keys exist."""
        assert validate_keys(sample_data)
        assert validate_keys(sample_non_usa_data)

    def test_validate_keys_no_topic(self, sample_data, sample_non_usa_data):
        """Checks that the function returns False if the topic key
        doesn't exist."""
        sample_data.pop("topic_arn")
        sample_non_usa_data.pop("topic_arn")
        assert not validate_keys(sample_data)
        assert not validate_keys(sample_non_usa_data)

    def test_validate_keys_no_magnitude(self, sample_data, sample_non_usa_data):
        """Checks that the function returns False if the magnitude key
        doesn't exist."""
        sample_data.pop("magnitude")
        sample_non_usa_data.pop("magnitude")
        assert not validate_keys(sample_data)
        assert not validate_keys(sample_non_usa_data)

    def test_validate_keys_no_state(self, sample_data, sample_non_usa_data):
        """Checks that the function returns False if the state key
        doesn't exist."""
        sample_data.pop("state_name")
        sample_non_usa_data.pop("state_name")
        assert not validate_keys(sample_data)
        assert not validate_keys(sample_non_usa_data)

    def test_validate_keys_no_region(self, sample_data, sample_non_usa_data):
        """Checks that the function returns False if the region key
        doesn't exist."""
        sample_data.pop("region_name")
        sample_non_usa_data.pop("region_name")
        assert not validate_keys(sample_data)
        assert not validate_keys(sample_non_usa_data)

    def test_validate_keys_no_time(self, sample_data, sample_non_usa_data):
        """Checks that the function returns False if the time key
        doesn't exist."""
        sample_data.pop("time")
        sample_non_usa_data.pop("time")
        assert not validate_keys(sample_data)
        assert not validate_keys(sample_non_usa_data)

    def test_validate_keys_no_tsunami(self, sample_data, sample_non_usa_data):
        """Checks that the function returns False if the tsunami key
        doesn't exist."""
        sample_data.pop("tsunami")
        sample_non_usa_data.pop("tsunami")
        assert not validate_keys(sample_data)
        assert not validate_keys(sample_non_usa_data)

    def test_validate_keys_no_latitude(self, sample_data, sample_non_usa_data):
        """Checks that the function returns False if the latitude key
        doesn't exist."""
        sample_data.pop("latitude")
        sample_non_usa_data.pop("latitude")
        assert not validate_keys(sample_data)
        assert not validate_keys(sample_non_usa_data)

    def test_validate_keys_no_longitude(self, sample_data, sample_non_usa_data):
        """Checks that the function returns False if the longitude key
        doesn't exist."""
        sample_data.pop("longitude")
        sample_non_usa_data.pop("longitude")
        assert not validate_keys(sample_data)
        assert not validate_keys(sample_non_usa_data)


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

    def test_validate_types_region_invalid(self, sample_data, sample_non_usa_data):
        """Checks that the function returns False if the region isn't
        of the correct datatype."""
        sample_data["region_name"] = 1
        sample_non_usa_data["region_name"] = 2
        assert not validate_types(sample_data)
        assert not validate_types(sample_non_usa_data)

    def test_validate_types_time_invalid(self, sample_data, sample_non_usa_data):
        """Checks that the function returns False if the time isn't
        of the correct datatype."""
        sample_data["time"] = 1
        sample_non_usa_data["time"] = 2
        assert not validate_types(sample_data)
        assert not validate_types(sample_non_usa_data)

    def test_validate_types_tsunami_invalid(self, sample_data, sample_non_usa_data):
        """Checks that the function returns False if the tsunami isn't
        of the correct datatype."""
        sample_data["tsunami"] = 1
        sample_non_usa_data["tsunami"] = 2
        assert not validate_types(sample_data)
        assert not validate_types(sample_non_usa_data)

    def test_validate_types_latitude_invalid(self, sample_data, sample_non_usa_data):
        """Checks that the function returns False if the latitude isn't
        of the correct datatype."""
        sample_data["latitude"] = 1
        sample_non_usa_data["latitude"] = 2
        assert not validate_types(sample_data)
        assert not validate_types(sample_non_usa_data)

    def test_validate_types_longitude_invalid(self, sample_data, sample_non_usa_data):
        """Checks that the function returns False if the longitude isn't
        of the correct datatype."""
        sample_data["longitude"] = 1
        sample_non_usa_data["longitude"] = 2
        assert not validate_types(sample_data)
        assert not validate_types(sample_non_usa_data)


class TestMakeMessage:
    """A class that groups together tests for make_message."""

    def test_make_message_returns_string(self, sample_data, sample_non_usa_data):
        """Checks that the function returns a string."""
        assert isinstance(make_message(sample_data), str)
        assert isinstance(make_message(sample_non_usa_data), str)

    def test_make_message_tsunami_true(self, sample_data, sample_non_usa_data):
        """Checks that tsunami information is included in the message
        if it is set to True."""
        sample_data["tsunami"] = True
        sample_non_usa_data["tsunami"] = True
        assert "tsunami" in make_message(sample_data)
        assert "tsunami" in make_message(sample_non_usa_data)

    def test_make_message_tsunami_false(self, sample_data, sample_non_usa_data):
        """Checks that tsunami information isn't included in the message
        if it set to False."""
        assert "tsunami" not in make_message(sample_data)
        assert "tsunami" not in make_message(sample_non_usa_data)


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
