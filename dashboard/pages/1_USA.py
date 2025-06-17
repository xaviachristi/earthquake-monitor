"""Module for displaying USA data page."""

from datetime import date

from pandas import DataFrame
from streamlit import (metric, title, multiselect,
                       columns, number_input,
                       date_input, altair_chart)

from data import (get_data, get_american_data,
                  get_mag_filtered_data,
                  get_date_filtered_data,
                  get_state_filtered_data)
from charts import (get_earthquakes_over_time,
                    get_average_mag,
                    get_earthquake_count_by_magnitude,
                    get_map_of_events,
                    get_total_number_of_earthquakes)


def filter_data(data: DataFrame,
                states: list[str],
                magnitude: int,
                start: date,
                end: date):
    """Return filtered data."""
    data = get_mag_filtered_data(data, magnitude)
    data = get_date_filtered_data(data, start, end)
    if states:
        data = get_state_filtered_data(data, states)
    return data


def display_charts(filtered_data: DataFrame):
    """Display to dashboard charts from filtered data."""
    altair_chart(get_map_of_events(filtered_data, "us"))
    altair_chart(get_earthquakes_over_time(filtered_data, "state"))
    altair_chart(get_earthquake_count_by_magnitude(filtered_data))
    col1, col2 = columns(2)
    with col1:
        metric(label="Total Number of Earthquakes",
               value=get_total_number_of_earthquakes(filtered_data))
    with col2:
        metric(label="Average Earthquake Magnitude",
               value=get_average_mag(filtered_data))


def serve_page():
    """Serve USA data page."""
    title("USA")
    data = get_data()
    us_data = get_american_data(data)
    states = us_data["state_name"].unique()

    state = None
    magnitude = None
    start = None
    stop = None

    col1, col2 = columns([0.6, 0.4])
    with col1:
        state = multiselect(label="Filter by State.",
                            options=states)
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
    filtered_data = filter_data(us_data, state, magnitude, start, stop)
    display_charts(filtered_data)


if __name__ == "__main__":
    serve_page()
