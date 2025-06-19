# pylint: skip-file
"""Tests for topic module."""

from unittest.mock import MagicMock, patch
from pandas import DataFrame
from math import isclose
from datetime import datetime

from topic import (
    get_topic_dictionaries,
    get_haversine_distance,
    get_dict_from_topic,
    get_applicable_topics,
    get_topics,
    is_point_in_circle
)


class TestGetHaversineDistance:
    def test_get_haversine_distance(self):
        dist = get_haversine_distance(51.5074, -0.1278, 48.8566, 2.3522)
        assert isclose(dist, 343, rel_tol=0.05)


class TestIsPointInCircle:
    def test_is_point_in_circle_true(self):
        assert is_point_in_circle(48.8566, 2.3522, 48.8566, 2.3522, 10)

    def test_is_point_in_circle_false(self):
        assert not is_point_in_circle(51.5074, -0.1278, 48.8566, 2.3522, 100)


class TestGetDictFromTopic:
    def test_get_dict_from_topic(self):
        topic_name = "c17-quake-65-p12345-m67890-100"
        arn = "arn:aws:sns:eu-west-1:123456789012:c17-quake-65-p12345-m67890-100"
        expected = {
            "topic_arn": arn,
            "magnitude": 6.5,
            "latitude": 1.2345,
            "longitude": -6.789,
            "radius": 100
        }
        result = get_dict_from_topic(topic_name, arn)
        assert result == expected


class TestGetApplicableTopics:
    def test_get_applicable_topics(self):
        topics = [{
            "topic_arn": "arn:test",
            "magnitude": 4.0,
            "latitude": 35.0,
            "longitude": 139.0,
            "radius": 500
        }]
        row = {
            "magnitude": 5.0,
            "latitude": 35.01,
            "longitude": 139.01,
            "state_name": "Tokyo",
            "region_name": "Kanto",
            "time": datetime(2023, 1, 1, 12, 0),
            "tsunami": 0
        }
        result = get_applicable_topics(topics, row)
        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0]["state_name"] == "Tokyo"


class TestGetTopics:
    @patch("topic.get_dict_from_topic")
    def test_get_topics(self, mock_get_dict):
        sns_mock = MagicMock()
        sns_mock.list_topics.side_effect = [
            {
                "Topics": [{"TopicArn": "arn:aws:sns:eu-west-1:123456789012:c17-quake-65-p12345-m67890-100"}],
                "NextToken": None
            }
        ]
        mock_get_dict.return_value = {
            "topic_arn": "arn:test",
            "magnitude": 6.5,
            "latitude": 1.2345,
            "longitude": -6.789,
            "radius": 100
        }
        result = get_topics(sns_mock)
        assert isinstance(result, list)
        assert result[0]["topic_arn"] == "arn:test"


class TestGetTopicDictionaries:
    @patch("topic.get_client")
    @patch("topic.get_topics")
    @patch("topic.get_applicable_topics")
    def test_get_topic_dictionaries(self, mock_get_applicable, mock_get_topics, mock_get_client):
        mock_get_client.return_value = MagicMock()
        mock_get_topics.return_value = [{
            "topic_arn": "arn:test",
            "magnitude": 4.0,
            "latitude": 35.0,
            "longitude": 139.0,
            "radius": 500
        }]
        mock_get_applicable.return_value = [{
            "topic_arn": "arn:test",
            "magnitude": 5.0,
            "state_name": "Tokyo",
            "region_name": "Kanto",
            "time": "2023-01-01 12:00",
            "tsunami": 0,
            "latitude": 35.01,
            "longitude": 139.01
        }]
        data = DataFrame([{
            "magnitude": 5.0,
            "latitude": 35.01,
            "longitude": 139.01,
            "state_name": "Tokyo",
            "region_name": "Kanto",
            "time": datetime(2023, 1, 1, 12, 0),
            "tsunami": 0
        }])
        result = get_topic_dictionaries(data)
        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0]["state_name"] == "Tokyo"
