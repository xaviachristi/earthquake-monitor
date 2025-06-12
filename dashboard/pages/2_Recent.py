"""Module for displaying the recent data page."""

from streamlit import (title, markdown,
                       columns, selectbox, slider)

from data import get_data


def serve_page():
    """Serve the recent page."""
    title("Recent")
    try:
        data = get_data()
        regions = data["region_name"].unique()
    except:
        data = None
        regions = ["Alabama", "Kentucky"]
    col1, col2, col3 = columns([0.25, 0.25, 0.5])
    with col1:
        region = selectbox(label="Filter by Region.",
                           options=regions)
    with col2:
        recency = selectbox(label="Select age of data.",
                            options=["Today", "7 days"])
    with col3:
        magnitude = slider(label="Filter by Minimum Magnitude.",
                           min_value=0, max_value=10, value=5)
    markdown("Placeholder for line chart of earthquake count over time.")
    col1, col2 = columns(2)
    with col1:
        markdown("Placeholder for recent earthquake details.")
    with col2:
        markdown("Placeholder for geographical map of recent events.")


if __name__ == "__main__":
    serve_page()
