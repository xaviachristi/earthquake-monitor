"""Module for Home page of dashboard."""

from dotenv import load_dotenv
import streamlit as st

from data import get_counts_by_region, get_data, get_counts_by_state
from charts import get_state_treemap, get_region_treemap


def serve_dash():
    """Serve streamlit dashboard."""
    load_dotenv()
    st.set_page_config(page_title="Earthquake Dashboard", layout="wide")
    st.title("Home")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            """
            This Dashboard presents historic earthquake data provided
            by the United States Geological Survey (USGS).
            There are two pages holding their respectively labelled data.
            On each page, there are filters on the top of the page to help 
            you change the data you are viewing.
            There are two pages - one for subscribing to alerts, 
            and another for viewing historical summary reports.
            \n**👈 Select a page from the sidebar** to view data insights.
            """
        )
    with col2:
        st.markdown(
            """
            This project aims to provide access to historical earthquake data 
            gathered by the USGS.
            USGS has an API that outputs data for up to the 
            previous month of earthquakes recorded.
            Our aim is to extract the most valuable data from that 
            and preserve it over time for our users.
            Our users can also subscribe to alert notifications for 
            earthquake events by region and/or magnitude of quake.
            Users can also view our reports section which contains a record 
            of daily summary reports of earthquake activity.
            """
        )
    try:
        earthquakes = get_data()
        if not earthquakes.empty:
            st.markdown("# Earthquake Quantity by State")
            state_counts = get_counts_by_state(earthquakes)
            fig = get_state_treemap(state_counts)
            st.plotly_chart(fig)

            st.markdown("# Earthquake Quantity by Region")
            state_counts = get_counts_by_region(earthquakes)
            fig = get_region_treemap(state_counts)
            st.plotly_chart(fig)
    except Exception as err:
        st.error(f"Cannot return data from database: {err}")


if __name__ == "__main__":
    serve_dash()
