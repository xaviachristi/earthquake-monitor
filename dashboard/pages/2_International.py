"""Module for displaying international data page."""

from datetime import date

from pandas import DataFrame
from streamlit import (metric, title, multiselect,
                       columns, number_input,
                       date_input, altair_chart,
                       slider, sidebar, image)

from data import (get_data, get_international_data,
                  get_mag_filtered_data,
                  get_date_filtered_data,
                  get_region_filtered_data)
from charts import (get_earthquakes_over_time,
                    get_average_mag,
                    get_earthquake_count_by_magnitude,
                    get_map_of_events,
                    get_total_number_of_earthquakes)


def filter_data(data: DataFrame,
                regions: list[str],
                magnitude: int,
                start: date,
                end: date):
    """Return filtered data."""
    data = get_mag_filtered_data(data, magnitude)
    data = get_date_filtered_data(data, start, end)
    if regions:
        data = get_region_filtered_data(data, regions)
    return data


def display_charts(filtered_data: DataFrame, zoom: int):
    """Display to dashboard charts from filtered data."""
    altair_chart(get_map_of_events(filtered_data, zoom, "global"))
    altair_chart(get_earthquakes_over_time(filtered_data, "region"))
    altair_chart(get_earthquake_count_by_magnitude(filtered_data))
    col1, col2 = columns(2)
    with col1:
        metric(label="Total Number of Earthquakes",
               value=get_total_number_of_earthquakes(filtered_data))
    with col2:
        metric(label="Average Earthquake Magnitude",
               value=get_average_mag(filtered_data))


def serve_page():
    """Serve International data page."""
    title("International")
    with sidebar:
        image("./dashboard/earthquake_monitor.png")
    data = get_data()
    inter_data = get_international_data(data)
    regions = inter_data["region_name"].unique()

    region = None
    magnitude = None
    start = None
    stop = None

    col1, col2 = columns([0.6, 0.4])
    with col1:
        region = multiselect(label="Filter by Country.",
                             options=regions)
        zoom = slider("Map Zoom.", min_value=0.1, value=1.0,
                      max_value=1.0, step=0.1)
    with col2:
        magnitude = number_input(
            "Minimum Magnitude", min_value=0.0, max_value=10.0,
            value="min", format="%0.1f", step=0.1)
        col3, col4 = columns(2)
        with col3:
            start = date_input(label="Start Date.",
                               value=date(year=2025, month=6, day=9),
                               max_value=date.today())
        with col4:
            stop = date_input(label="End Date.",
                              value="today",
                              max_value=date.today())
    filtered_data = filter_data(inter_data, region, magnitude, start, stop)
    display_charts(filtered_data, zoom)


if __name__ == "__main__":
    serve_page()
