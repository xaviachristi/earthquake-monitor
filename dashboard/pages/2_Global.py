"""Module for displaying the global data page."""

from streamlit import (title, markdown,
                       columns, selectbox, number_input)

from data import get_data, get_american_data, get_international_data


def serve_page():
    """Serve the global data page."""
    title("Global")
    data = get_data()
    global_data = get_international_data(data)
    regions = global_data["regions"].unique()
    col1, col2, col3 = columns([0.25, 0.25, 0.5])
    with col1:
        region = selectbox(label="Filter by Region.",
                           options=regions)
    with col2:
        recency = selectbox(label="Select age of data.",
                            options=["Today", "7 days"])
    with col3:
        magnitude = number_input(
            "Minimum Magnitude", min_value=0.0, max_value=10.0,
            value="min", format="%0.1f", step=0.1)
    markdown("Placeholder for line chart of earthquake count over time.")
    col1, col2 = columns(2)
    with col1:
        markdown("Placeholder for recent earthquake details.")
    with col2:
        markdown("Placeholder for geographical map of recent events.")


if __name__ == "__main__":
    serve_page()
