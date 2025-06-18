"""Unit tests for app.py."""

from unittest.mock import patch, MagicMock

from app import app


@patch("app.get_connection")
@patch("app.query_database")
def test_site_index_success(fake_query_database, fake_get_connection,
                            get_test_client):
    """Checks the index returns a documentation page."""

    testing_client = get_test_client
    response = testing_client.get('/')

    assert response.status_code == 200
    assert b"Documentation" in response.data


@patch("app.CONN", MagicMock())
@patch("app.get_connection")
@patch("app.query_database")
def test_site_earthquake_blank(fake_query_database, fake_get_connection, 
                                get_test_client):
    """Checks the earthquake endpoint returns 204 if data is empty."""

    fake_query_database.return_value = {}
    fake_get_connection.return_value = MagicMock()

    testing_client = get_test_client
    response = testing_client.get('/earthquakes')

    assert response.status_code == 204


@patch("app.CONN", MagicMock())
@patch("app.get_connection")
@patch("app.query_database")
def test_site_earthquake_returns_json(fake_query_database, fake_get_connection,
                                      get_test_client, example_response):
    """Checks the earthquake endpoint returns 200."""

    fake_query_database.return_value = example_response
    fake_get_connection.return_value = MagicMock()

    testing_client = get_test_client
    response = testing_client.get('/earthquakes')

    assert response.status_code == 200
