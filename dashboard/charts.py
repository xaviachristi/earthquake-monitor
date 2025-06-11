"""Module for serving visualisations needed for dashboard pages."""

from logging import getLogger, basicConfig

from streamlit import cache_resource
from pandas import DataFrame
from plotly.express import treemap, Constant


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
        path=[Constant("all"), 'State Name'],
        values="Earthquake Count")
    fig.update_traces(root_color="lightgrey")
    fig.update_layout(margin={"t": 50, "l": 25, "r": 25, "b": 25})
    return fig
