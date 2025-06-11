"""Fixtures for tests in this directory."""

import pytest
import obspy

@pytest.fixture
def example_catalog():
    return obspy.core.event.catalog._create_example_catalog()
