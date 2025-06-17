"""Module for serving visualisations needed for dashboard pages."""

from logging import getLogger, basicConfig

from pandas import DataFrame
from plotly.express import treemap
from altair import (Chart, X, Y, Color, Scale, topo_feature, Tooltip)


logger = getLogger(__name__)

basicConfig(
    level="WARNING",
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S"
)


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


def get_earthquakes_over_time_for_states(data: DataFrame) -> Chart:
    """Return chart of earthquake counts over time using Altair's internal aggregation."""
    line = Chart(data).mark_line().encode(
        x=X("yearmonthdate(time):T", title="Date"),
        y=Y("count():Q", title="Number of Earthquakes"),
        color=Color("state_name:N", title="State")
    )

    points = Chart(data).mark_circle(size=30).encode(
        x="yearmonthdate(time):T",
        y="count():Q",
        color="state_name:N",
        tooltip=[
            Tooltip("yearmonthdate(time):T", title="Date"),
            Tooltip("state_name:N", title="State"),
            Tooltip("count():Q", title="Number of Earthquakes")
        ]
    )

    return (line + points).properties(
        title="Earthquakes Over Time",
        width=800,
        height=400
    )


def get_earthquakes_over_time_for_regions(data: DataFrame) -> Chart:
    """Return chart of earthquake counts over time using Altair's internal aggregation."""
    line = Chart(data).mark_line().encode(
        x=X("yearmonthdate(time):T", title="Date"),
        y=Y("count():Q", title="Number of Earthquakes"),
        color=Color("region_name:N", title="Country")
    )

    points = Chart(data).mark_circle(size=30).encode(
        x="yearmonthdate(time):T",
        y="count():Q",
        color="region_name:N",
        tooltip=[
            Tooltip("yearmonthdate(time):T", title="Date"),
            Tooltip("region_name:N", title="Region"),
            Tooltip("count():Q", title="Number of Earthquakes")
        ]
    )

    return (line + points).properties(
        title="Earthquakes Over Time",
        width=800,
        height=500
    )


def get_earthquake_count_by_magnitude(data: DataFrame) -> Chart:
    """Return bar chart of earthquake counts per rounded magnitude."""
    data['rounded_mag'] = data['magnitude'].astype(float).round(1)
    return Chart(data).mark_bar().encode(
        x=X("rounded_mag:Q", title="Magnitude").scale(domain=[0, 10]),
        y=Y("count():Q", title="Number of Earthquakes"),
        tooltip=["rounded_mag", "count()"]
    ).properties(
        title="Earthquake Count by Magnitude"
    )


def get_average_mag(data: DataFrame) -> float:
    """Return average magnitude of earthquakes."""
    return round(data['magnitude'].mean(), 2)


def get_total_number_of_earthquakes(data: DataFrame) -> int:
    return len(data)


def get_american_map_of_events(data: DataFrame) -> Chart:
    """Return a geographical map of earthquake events over the U.S."""
    data['latitude'] = data['latitude'].astype(float)
    data['longitude'] = data['longitude'].astype(float)
    data['magnitude'] = data['magnitude'].astype(float)

    world_map = topo_feature(
        'https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json', 'countries')

    # Base map of world
    base = Chart(world_map).mark_geoshape(
        fill='lightgray',
        stroke='white'
    ).project(
        type='mercator',
        center=[-100, 40],
        scale=200
    ).properties(
        width=900,
        height=600
    )

    # Earthquake points
    points = Chart(data).mark_circle(size=30).encode(
        longitude='longitude:Q',
        latitude='latitude:Q',
        color=Color('magnitude:Q', scale=Scale(
            scheme='yelloworangered'), title="Magnitude"),
        tooltip=['time:T', 'latitude:Q', 'longitude:Q', 'magnitude:Q']
    ).project(
        type='mercator',
        center=[-100, 40],
        scale=200
    ).properties(
        width=900,
        height=600
    )

    # Combine layers
    return base + points


def get_global_map_of_events(data: DataFrame) -> Chart:
    """Return a geographical map of earthquake events over the U.S."""
    data['latitude'] = data['latitude'].astype(float)
    data['longitude'] = data['longitude'].astype(float)
    data['magnitude'] = data['magnitude'].astype(float)

    world_map = topo_feature(
        'https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json', 'countries')

    # Base map of world
    base = Chart(world_map).mark_geoshape(
        fill='lightgray',
        stroke='white'
    ).project(
        type='naturalEarth1'
    ).properties(
        width=900,
        height=600
    )

    # Earthquake points
    points = Chart(data).mark_circle(size=30).encode(
        longitude='longitude:Q',
        latitude='latitude:Q',
        color=Color('magnitude:Q', scale=Scale(
            scheme='yelloworangered'), title="Magnitude"),
        tooltip=['time:T', 'latitude:Q', 'longitude:Q', 'magnitude:Q']
    ).project(
        type='naturalEarth1'
    ).properties(
        width=900,
        height=600
    )

    # Combine layers
    return base + points
