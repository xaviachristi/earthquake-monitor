# pylint: skip-file

"""Unit tests for app_functions.py."""

from app_functions import (can_be_converted_to_float, validate_magnitude,
                           validate_time, prepare_query_arguments)
from datetime import datetime

from pytest import raises


class TestCanBeConvertedToFloat:
    """Tests for the pure function can_be_converted_to_float()."""

    def test_can_be_converted_to_float_pos_1(self):
        assert can_be_converted_to_float("0.0") == True

    def test_can_be_converted_to_float_pos_2(self):
        assert can_be_converted_to_float("0")

    def test_can_be_converted_to_float_pos_3(self):
        assert can_be_converted_to_float("-4")

    def test_can_be_converted_to_float_pos_4(self):
        assert can_be_converted_to_float("4109248.4534")

    def test_can_be_converted_to_float_pos_5(self):
        assert can_be_converted_to_float(3.1)

    def test_can_be_converted_to_float_pos_6(self):
        assert can_be_converted_to_float("7.6")


    def test_can_be_converted_to_float_neg_1(self):
        assert not can_be_converted_to_float("0.0.0")

    def test_can_be_converted_to_float_neg_2(self):
        assert not can_be_converted_to_float("Greg") 

    def test_can_be_converted_to_float_neg_3(self):
        assert not can_be_converted_to_float([0.0, 5])

    def test_can_be_converted_to_float_neg_4(self):
        assert not can_be_converted_to_float("4109248.453p4")

    def test_can_be_converted_to_float_neg_5(self):
        assert not can_be_converted_to_float("eeee")

    def test_can_be_converted_to_float_neg_6(self):
        assert not can_be_converted_to_float((0.1, 6.4))


class TestValidateMagnitude:
    """Test for validate_magnitude()."""

    def test_validate_magnitude_pos_1(self):
        assert validate_magnitude(10)

    def test_validate_magnitude_pos_2(self):
        assert validate_magnitude(1.0)

    def test_validate_magnitude_pos_2(self):
        assert validate_magnitude(4.5)


    def test_validate_magnitude_value_errors_1(self):
        with raises(ValueError):
            validate_magnitude(12)

    def test_validate_magnitude_value_errors_2(self):
        with raises(ValueError):
            validate_magnitude(-1)

    def test_validate_magnitude_value_errors_3(self):
        with raises(ValueError):
            validate_magnitude(-1000000.1)

    def test_validate_magnitude_value_errors_4(self):
        with raises(ValueError):
            validate_magnitude(999999999999)


    def test_validate_magnitude_type_errors_1(self):
        with raises(TypeError):
            validate_magnitude("12")

    def test_validate_magnitude_type_errors_2(self):
        with raises(TypeError):
            validate_magnitude("1.0")

    def test_validate_magnitude_type_errors_3(self):
        with raises(TypeError):
            validate_magnitude("10")

    def test_validate_magnitude_type_errors_4(self):
        with raises(TypeError):
            validate_magnitude("helmp")

    def test_validate_magnitude_type_errors_5(self):
        with raises(TypeError):
            validate_magnitude(False)


class TestValidateTime:

    def test_validate_time_pos_1(self):
        assert validate_time(datetime.now().isoformat())

    def test_validate_time_pos_2(self):
        assert validate_time("2025-06-16T12:34:54.824Z")

    def test_validate_time_pos_3(self):
        assert validate_time("1979-01-16T02:11:00")

    def test_validate_time_value_errors_1(self):
        with raises(ValueError):
            validate_time("2025-06-16T12:74:00")

    def test_validate_time_type_errors_1(self):
        with raises(TypeError):
            validate_time(20120472161700)


class TestValidateApiQueryArgumentNames:
    # def test_validate_api_query_argument_names_1(self):
    pass


class TestGetQueryTemplate:
    pass


class TestPrepareQueryArguments:

    def test_prepare_query_arguments_adds_defaults(self):
        assert {"magnitude", "start_time", "end_time"}.issubset(
            prepare_query_arguments({}))

    def test_prepare_query_arguments_magnitude(self):
        prepared_arguments = prepare_query_arguments({"mag": "5.1"})
        assert prepared_arguments["magnitude"] == "5.1"


class TestQueryDatabase:
    pass


class TestFormatSQLResponseAsJSON:
    pass
