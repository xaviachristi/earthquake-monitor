# pylint: skip-file

from pytest import fixture

from app import app


@fixture(scope="module")
def get_test_client():
    return app.test_client()
