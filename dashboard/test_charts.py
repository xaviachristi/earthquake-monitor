# pylint: skip-file
"""Tests for charts module."""

from altair import Chart, LayerChart
from plotly.graph_objs import Figure

from charts import (
    get_average_mag,
    get_total_number_of_earthquakes,
    get_earthquake_count_by_magnitude,
    get_earthquakes_over_time,
    get_region_treemap,
    get_state_choropleth,
    get_map_of_events
)


class TestGetAverageMag:
    def test_get_average_mag(self, sample_data):
        result = get_average_mag(sample_data)
        assert isinstance(result, float)
        assert round(result, 2) == round(sample_data['magnitude'].mean(), 2)


class TestGetTotalNumberOfEarthquakes:
    def test_get_total_number_of_earthquakes(self, sample_data):
        result = get_total_number_of_earthquakes(sample_data)
        assert isinstance(result, int)
        assert result == len(sample_data)


class TestGetEarthquakeCountByMagnitude:
    def test_get_earthquake_count_by_magnitude(self, sample_data):
        chart = get_earthquake_count_by_magnitude(sample_data)
        assert isinstance(chart, Chart)
        assert chart.mark == 'bar'


class TestGetEarthquakesOverTime:
    def test_get_earthquakes_over_time_region(self, sample_data):
        chart = get_earthquakes_over_time(sample_data, group_by="region")
        assert isinstance(chart, LayerChart)

    def test_get_earthquakes_over_time_state(self, sample_data):
        chart = get_earthquakes_over_time(sample_data, group_by="state")
        assert isinstance(chart, LayerChart)


class TestGetRegionTreemap:
    def test_get_region_treemap(self, sample_data):
        fig = get_region_treemap(sample_data)
        assert isinstance(fig, Figure)
        assert fig.data


class TestGetStateChoropleth:
    def test_get_state_choropleth(self, sample_data):
        fig = get_state_choropleth(sample_data)
        assert isinstance(fig, Figure)
        assert fig.data


class TestGetMapOfEvents:
    def test_get_map_of_events_us(self, sample_data):
        fig = get_map_of_events(sample_data, zoom=1, scope="us")
        assert isinstance(fig, LayerChart)

    def test_get_map_of_events_global(self, sample_data):
        fig = get_map_of_events(sample_data, zoom=1, scope="global")
        assert isinstance(fig, LayerChart)
