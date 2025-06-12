"""Module for loading pipeline data into a database."""

from logging import getLogger, basicConfig

from dotenv import load_dotenv
from pandas import DataFrame, Series
from psycopg import Connection, connect


logger = getLogger(__name__)

basicConfig(
    level="DEBUG",
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S"
)


def get_connection() -> Connection:
    """Return connection to database."""


def get_current_db(conn: Connection) -> DataFrame:
    """Return all records currently in database."""


def get_diff(df1: DataFrame, df2: DataFrame) -> DataFrame:
    """Return records that only exist in first DataFrame."""
    df_diff = df1.merge(df2, how='left', indicator=True)
    return df_diff[df_diff['_merge'] == 'left_only'].drop(columns=['_merge'])


def upload_to_db(conn: Connection, data: DataFrame):
    """Upload DataFrame to database."""


def load_quakes(quakes: DataFrame) -> DataFrame:
    """Return earthquakes that have been uploaded to the database."""
    logger.info("Getting database connection...")
    db_conn = get_connection()

    logger.info("Getting data already in database...")
    old_quakes = get_current_db(db_conn)
    logger.debug("Found old earthquake data...\n%s", old_quakes)

    logger.info("Identifying new earthquake data...")
    new_quakes = get_diff(quakes, old_quakes)
    logger.debug("Found new earthquake data...\n%s", new_quakes)

    logger.info("Uploading new data to database...")
    upload_to_db(db_conn, new_quakes)

    return new_quakes


if __name__ == "__main__":
    load_dotenv()
    load_quakes()
