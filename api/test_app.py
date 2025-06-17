"""Unit tests for app.py."""

from unittest.mock import patch

from app import app


@patch("app.get_connection")
@patch("app.query_database")
def test_site_index_success(fake_query_database, fake_get_connection, get_test_client):
    """Checks the index returns a documentation page."""

    # fake_query_database =
    # fake_get_connection = 

    testing_client = get_test_client
    response = testing_client.get('/')

    assert response.status_code == 200
    assert b"Documentation" in response.data
