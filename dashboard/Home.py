"""Module for Home page of dashboard."""

from logging import getLogger, basicConfig

from dotenv import load_dotenv
from data import get_data, get_counts_by_state
from charts import get_state_treemap
import streamlit as st


def serve_dash():
    """Serve streamlit dashboard."""
    st.set_page_config(page_title="Home", layout="wide")
    st.title("Home")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            """
            This Dashboard presents historic earthquake data provided by USGS.
            There are two pages holding their respectively labelled data.
            On each page, there are filters on the top of the page to help you change the data you are viewing.
            There are another two pages for subscribing for alerts and viewing historic summary reports.
            \n**👈 Select a page from the sidebar** to see data insights.
            """
        )
    with col2:
        st.markdown(
            """
            This project aims to provide access to historical earthquake data gathered by the United States Geological Survey.
            USGS has an API that outputs data for up to the previous month of earthquakes recorded.
            Our aim is to extract the most valuable data from that and preserve it over time for our users.
            Our users can also subscribe to alert notifcations for earthquake events by region and/or magintude of quake.
            Users can also view our reports section which contains a record of daily summary reports of earthquake activity.
            """
        )
    earthquakes = get_data()
    if earthquakes:
        st.markdown("#Earthquake Quantity by State")
        state_counts = get_counts_by_state(earthquakes)
        fig = get_state_treemap(state_counts)
        fig.show()


if __name__ == "__main__":
    load_dotenv()
    serve_dash()
    logger = getLogger(__name__)

    basicConfig(
        level="WARNING",
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S"
    )
