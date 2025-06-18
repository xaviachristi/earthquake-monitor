"""Module for handling data from the RDS."""

from datetime import date
from os import environ as ENV
from logging import getLogger, basicConfig

from dotenv import load_dotenv
from pandas import DataFrame
from psycopg import Connection, connect, rows
from numpy import where


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
    data = data.copy()
    logger.info("Grouping DataFrame by state...")
    return data["state_name"].value_counts().rename_axis("State Name").reset_index(name="Earthquake Count")


def get_counts_by_region(data: DataFrame) -> DataFrame:
    """Return dataframes of value counts for each region."""
    data = data.copy()
    logger.info("Grouping DataFrame by region...")
    return (data[["region_name", "state_name"]].value_counts()
            .rename_axis(["Region Name", "State Name"])
            .reset_index(name="Earthquake Count"))


def get_american_data(data: DataFrame) -> DataFrame:
    """Return dataframe filtered fpr US data only."""
    data = data.copy()
    logger.info("Grouping DataFrame if from US...")
    return data[data["state_name"] != "Not in the USA"]


def get_international_data(data: DataFrame) -> DataFrame:
    """Return dataframe filtered for international data only."""
    data = data.copy()
    logger.info("Masking data for us and non us...")
    data["region_name"] = where(data["state_name"] != "Not in the USA",
                                "USA",
                                data["region_name"])
    return data


def get_mag_filtered_data(data: DataFrame, mag: int) -> DataFrame:
    """Return magnitude filtered data with mag as a minimum magnitude."""
    data = data.copy()
    logger.info("Filtering data by magnitude now...")
    return data[data["magnitude"] >= mag]


def get_date_filtered_data(data: DataFrame, start: date, end: date) -> DataFrame:
    """Return date filtered data with start and end date."""
    data = data.copy()
    logger.info("Filtering data by date now...")
    mask = (data["time"].dt.date >= start) & (data["time"].dt.date <= end)
    return data[mask]


def get_state_filtered_data(data: DataFrame, states: list[str]) -> DataFrame:
    """Return state filtered data with states as list of accepted names."""
    data = data.copy()
    logger.info("Filtering data by states now...")
    return data[data["state_name"].isin(states)]


def get_region_filtered_data(data: DataFrame, regions: list[str]) -> DataFrame:
    """Return region filtered data with regions as list of accepted names."""
    data = data.copy()
    logger.info("Filtering data by regions now...")
    return data[data["region_name"].isin(regions)]


if __name__ == "__main__":
    load_dotenv()
    all_data = get_data()
    print(all_data)
