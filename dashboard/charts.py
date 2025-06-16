"""Module for serving visualisations needed for dashboard pages."""

from logging import getLogger, basicConfig

from streamlit import cache_resource
from pandas import DataFrame
from plotly.express import treemap
from altair import Chart, X, Y, Color


logger = getLogger(__name__)

basicConfig(
    level="WARNING",
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S"
)


@cache_resource
def get_state_treemap(data: DataFrame) -> treemap:
    """Return treemap of counts of events per state."""
    logger.info("Creating treemap...")
    fig = treemap(
        data_frame=data,
        path=['State Name'],
        values="Earthquake Count",
        custom_data=['State Name', 'Earthquake Count'])
    fig.update_traces(
        root_color="lightgrey",
        hovertemplate=(
            "<b>%{customdata[0]}</b><br>" +
            "Earthquake Count: %{customdata[1]}<extra></extra>"
        )
    )
    fig.update_layout(margin={"t": 50, "l": 25, "r": 25, "b": 25})
    return fig


@cache_resource
def get_region_treemap(data: DataFrame) -> treemap:
    """Return treemap of counts of events per region."""
    logger.info("Creating treemap...")
    fig = treemap(
        data_frame=data,
        path=['Region Name'],
        values="Earthquake Count",
        custom_data=['Region Name', 'Earthquake Count'])
    fig.update_traces(
        root_color="lightgrey",
        hovertemplate=(
            "<b>%{customdata[0]}</b><br>" +
            "Earthquake Count: %{customdata[1]}<extra></extra>"
        )
    )
    fig.update_layout(margin={"t": 50, "l": 25, "r": 25, "b": 25})
    return fig


@cache_resource
def get_earthquakes_over_time(data: DataFrame) -> Chart:
    """Return chart of earthquake counts over time using Altair's internal aggregation."""
    return Chart(data).mark_line().encode(
        x=X("yearmonthdate(time):T", title="Date"),
        y=Y("count():Q", title="Number of Earthquakes"),
        color=Color("state_name:N", title="State")
    ).properties(
        title="Earthquakes Over Time"
    )


def get_earthquake_count_by_magnitude(data: DataFrame) -> Chart:
    """Return chart of earthquake counts per magnitude earthquake."""


def get_average_mag(data: DataFrame) -> int:
    """Return average magnitude of earthquake."""


def get_total_number_of_earthquakes(data: DataFrame) -> Chart:
    """Return chart of earthquake counts per magnitude earthquake."""


def get_geographical_map_of_events(data: DataFrame) -> Chart:
    """Return chart of earthquake counts per magnitude earthquake."""
