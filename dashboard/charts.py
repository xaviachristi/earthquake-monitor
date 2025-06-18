"""Module for serving visualisations needed for dashboard pages."""

from logging import getLogger, basicConfig

from pandas import DataFrame
from plotly.express import treemap, choropleth, colors
from altair import (Chart, X, Y, Color, Scale, topo_feature, Tooltip)
from pycountry import countries


logger = getLogger(__name__)

basicConfig(
    level="WARNING",
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S"
)


def get_state_treemap(data: DataFrame) -> treemap:
    """Return treemap of counts of events per state."""
    logger.info("Creating treemap...")
    us_state_to_abbrev = {
        "Alabama": "AL",
        "Alaska": "AK",
        "Arizona": "AZ",
        "Arkansas": "AR",
        "California": "CA",
        "Colorado": "CO",
        "Connecticut": "CT",
        "Delaware": "DE",
        "Florida": "FL",
        "Georgia": "GA",
        "Hawaii": "HI",
        "Idaho": "ID",
        "Illinois": "IL",
        "Indiana": "IN",
        "Iowa": "IA",
        "Kansas": "KS",
        "Kentucky": "KY",
        "Louisiana": "LA",
        "Maine": "ME",
        "Maryland": "MD",
        "Massachusetts": "MA",
        "Michigan": "MI",
        "Minnesota": "MN",
        "Mississippi": "MS",
        "Missouri": "MO",
        "Montana": "MT",
        "Nebraska": "NE",
        "Nevada": "NV",
        "New Hampshire": "NH",
        "New Jersey": "NJ",
        "New Mexico": "NM",
        "New York": "NY",
        "North Carolina": "NC",
        "North Dakota": "ND",
        "Ohio": "OH",
        "Oklahoma": "OK",
        "Oregon": "OR",
        "Pennsylvania": "PA",
        "Rhode Island": "RI",
        "South Carolina": "SC",
        "South Dakota": "SD",
        "Tennessee": "TN",
        "Texas": "TX",
        "Utah": "UT",
        "Vermont": "VT",
        "Virginia": "VA",
        "Washington": "WA",
        "West Virginia": "WV",
        "Wisconsin": "WI",
        "Wyoming": "WY",
        "District of Columbia": "DC",
        "American Samoa": "AS",
        "Guam": "GU",
        "Northern Mariana Islands": "MP",
        "Puerto Rico": "PR",
        "United States Minor Outlying Islands": "UM",
        "Virgin Islands, U.S.": "VI",
    }
    data["State Name"] = data["State Name"].map(us_state_to_abbrev)
    fig = choropleth(data,
                     locations="State Name",
                     locationmode="USA-states",
                     color="Earthquake Count",
                     scope="usa")
    fig.update_layout(margin={"t": 50, "l": 25, "r": 25, "b": 25})
    return fig


def get_region_treemap(data: DataFrame) -> treemap:
    """Return treemap of counts of events per region."""
    logger.info("Creating treemap...")
    data = data.copy()
    data = data[data["Region Name"] != "No Country"]
    data["Region Name"] = data["Region Name"].replace("Turkey", "Turkiye")
    data["Region Name"] = data["Region Name"].apply(
        lambda x: countries.search_fuzzy(x)[0].alpha_3)
    fig = choropleth(data, locations="Region Name",
                     color="Earthquake Count",
                     hover_name="Region Name",
                     color_continuous_scale=colors.sequential.Plasma)
    fig.update_layout(margin={"t": 50, "l": 25, "r": 25, "b": 25})
    return fig


def get_earthquakes_over_time(data: DataFrame, group_by: str = "region") -> Chart:
    """Return chart of earthquake counts over time grouped by state or region."""
    group_field = f"{group_by}_name:N"
    group_title = group_by.capitalize()

    line = Chart(data).mark_line().encode(
        x=X("yearmonthdate(time):T", title="Date"),
        y=Y("count():Q", title="Number of Earthquakes"),
        color=Color(group_field, title=group_title)
    )

    points = Chart(data).mark_circle(size=30).encode(
        x="yearmonthdate(time):T",
        y="count():Q",
        color=group_field,
        tooltip=[
            Tooltip("yearmonthdate(time):T", title="Date"),
            Tooltip(group_field, title=group_title),
            Tooltip("count():Q", title="Number of Earthquakes")
        ]
    )

    return (line + points).properties(
        title="Earthquakes Over Time",
        width=800,
        height=600 if group_by == "region" else 500
    )


def get_earthquake_count_by_magnitude(data: DataFrame) -> Chart:
    """Return bar chart of earthquake counts per rounded magnitude."""
    data['rounded_mag'] = data['magnitude'].astype(float).round(1)
    return Chart(data).mark_bar().encode(
        x=X("rounded_mag:Q", title="Magnitude").scale(domain=[0, 10]),
        y=Y("count():Q", title="Number of Earthquakes"),
        tooltip=[Tooltip("rounded_mag", title="Magnitude"),
                 Tooltip("count()", title="Number of Earthquakes")]
    ).properties(
        title="Earthquake Count by Magnitude"
    )


def get_average_mag(data: DataFrame) -> float:
    """Return average magnitude of earthquakes."""
    return round(data['magnitude'].mean(), 2)


def get_total_number_of_earthquakes(data: DataFrame) -> int:
    """Return total number of earthquakes."""
    return len(data)


def get_map_of_events(data: DataFrame, zoom: int, scope: str = "global") -> Chart:
    """Return a geographical map of earthquake events over the U.S."""
    data = data.copy()
    data['latitude'] = data['latitude'].astype(float)
    data['longitude'] = data['longitude'].astype(float)
    data['magnitude'] = data['magnitude'].astype(float)

    world_map = topo_feature(
        'https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json', 'countries')

    if scope == "us":
        projection = 'mercator'
        center = [-100, 40]
        scale = 200*zoom
    else:
        projection = 'naturalEarth1'
        center = [0, 0]
        scale = 200*zoom

    # Base map
    base = Chart(world_map).mark_geoshape(
        fill='lightgray',
        stroke='white'
    ).project(
        type=projection,
        center=center,
        scale=scale
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
        type=projection,
        center=center,
        scale=scale
    ).properties(
        width=900,
        height=600
    )

    return base + points
