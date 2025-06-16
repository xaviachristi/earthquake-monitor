"""Module for handling data from the RDS."""

from os import environ as ENV
from logging import getLogger, basicConfig

from dotenv import load_dotenv
from pandas import DataFrame
from psycopg import Connection, connect, rows
from streamlit import cache_data


logger = getLogger(__name__)

basicConfig(
    level="WARNING",
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S"
)


def get_connection() -> Connection:
    """Return a db connection using environment variables."""
    logger.info("Getting DB connection...")
    return connect(
        host=ENV["DB_HOST"],
        user=ENV["DB_USER"],
        dbname=ENV["DB_NAME"],
        port=int(ENV["DB_PORT"]),
        password=ENV["DB_PASSWORD"],
        row_factory=rows.dict_row
    )


@cache_data
def get_data() -> DataFrame:
    """Return all data for dashboard from the RDS."""
    logger.info("Getting results from DB...")
    with get_connection() as con:
        with con.cursor() as curs:
            curs.execute("""SELECT * FROM earthquake
                         JOIN "state_region_interaction" USING(state_region_interaction_id)
                         JOIN "state" USING (state_id) 
                         JOIN "region" USING (region_id);""")
            quakes = curs.fetchall()
    return DataFrame.from_dict(quakes)


def get_counts_by_state(data: DataFrame) -> DataFrame:
    """Return dataframes of value counts for each state."""
    logger.info("Grouping DataFrame by state...")
    return data["state_name"].value_counts().rename_axis("State Name").reset_index(name="Earthquake Count")


def get_counts_by_region(data: DataFrame) -> DataFrame:
    """Return dataframes of value counts for each region."""
    logger.info("Grouping DataFrame by region...")
    return data["region_name"].value_counts().rename_axis("Region Name").reset_index(name="Earthquake Count")


if __name__ == "__main__":
    load_dotenv()
    all_data = get_data()
    print(all_data)
