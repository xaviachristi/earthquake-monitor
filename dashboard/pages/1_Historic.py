"""Module for displaying historic data page."""

from datetime import date

from streamlit import (title, sidebar, markdown,
                       columns, selectbox, slider,
                       date_input)

from data import get_data


def serve_page():
    """Serve Realtime page."""
    title("Historic")
    try:
        data = get_data()
        regions = data["region_name"].unique()
    except:
        data = None
        regions = ["Alabama", "Kentucky"]
    col1, col2, col3, col4 = columns([0.25, 0.15, 0.15, 0.4])
    with col1:
        region = selectbox(label="Filter by Region.",
                           options=regions)
    with col2:
        start = date_input(label="Start Date.",
                           value=date(year=2025, month=6, day=9),
                           max_value=date.today())
    with col3:
        stop = date_input(label="End Date.",
                          value="today",
                          max_value=date.today())
    with col4:
        magnitude = slider(label="Filter by Minimum Magnitude.",
                           min_value=0, max_value=10, value=5)
    markdown("Placeholder for rline chart fo earthquake count over time.")
    col1, col2 = columns(2)
    with col1:
        markdown("Placeholder for recent earthquake details.")
    with col2:
        markdown("Placeholder for geographical map of recent events.")


if __name__ == "__main__":
    serve_page()
