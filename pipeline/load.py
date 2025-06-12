"""Module for loading pipeline data into a database."""

from os import environ as ENV
from logging import getLogger, basicConfig

from dotenv import load_dotenv
from pandas import DataFrame
from psycopg import Connection, connect, rows, DatabaseError


logger = getLogger(__name__)

basicConfig(
    level="DEBUG",
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S"
)


def get_connection() -> Connection:
    """Return connection to database."""
    return connect(
        host=ENV["DB_HOST"],
        user=ENV["DB_USER"],
        dbname=ENV["DB_NAME"],
        port=int(ENV["DB_PORT"]),
        password=ENV["DB_PASSWORD"],
        row_factory=rows.dict_row
    )


def get_current_db(conn: Connection) -> DataFrame:
    """Return all records currently in database."""
    with conn.cursor() as curs:
        curs.execute("""SELECT * FROM earthquake_details
                        JOIN "state" USING (state_id) 
                        JOIN "region" USING (region_id);""")
        quakes = curs.fetchall()
    return DataFrame(quakes).drop(columns=["state_id", "region_id"])


def get_diff(df1: DataFrame, df2: DataFrame) -> DataFrame:
    """Return records that only exist in first DataFrame."""
    df1 = df1.drop(columns=["earthquake_id"])
    df2 = df2.drop(columns=["earthquake_id"])
    df_diff = df1.merge(df2, how='left', indicator=True)
    return df_diff[df_diff['_merge'] == 'left_only'].drop(columns=['_merge'])


def get_region_id(conn: Connection, region: str) -> int | None:
    """Return id of region if it is in the database."""
    with conn.cursor() as curs:
        curs.execute("""SELECT * FROM region 
                     WHERE region_name = %s;""",
                     (region,))
        result = curs.fetchone()
    if result:
        return result[0]
    return None


def get_state_id(conn: Connection, state: str) -> int | None:
    """Return id of state if it is in the database."""
    with conn.cursor() as curs:
        curs.execute("""SELECT * FROM "state" 
                     WHERE state_name = %s;""",
                     (state,))
        result = curs.fetchone()
    if result:
        return result[0]
    return None


def upload_row_to_db(conn: Connection, row: dict):
    """Upload row as a dictionary to the database."""
    logger.info("Uploading row with id: %s", row["earthquake_id"])

    logger.info("Checking if region is in database...")
    region_id = get_region_id(conn, row["region_name"])

    if not region_id:
        logger.info("Uploading region data...")
        with conn.cursor() as curs:
            curs.execute("""INSERT INTO region(region_name)
                        VALUES (%s)
                        RETURNING region_id;""",
                         (row["region_name"],))
            region_id = curs.fetchone()[0]

    logger.info("Checking if state is in database...")
    state_id = get_state_id(conn, row["state_name"])

    if not state_id:
        logger.info("Uploading state data...")
        with conn.cursor() as curs:
            curs.execute("""INSERT INTO state(state_name, region_id)
                        VALUES (%s, %s)
                        RETURNING state_id;""",
                         (row["state_name"], region_id))
            state_id = curs.fetchone()[0]

    logger.info("Uploading earthquake data...")
    with conn.cursor() as curs:
        curs.execute("""INSERT INTO earthquake(magnitude,
                     latitude, longitude, "time", updated, depth,
                     "url", felt, tsunami, cdi, mmi, nst,
                     sig, net, dmin, alert, location_source,
                     magnitude_type, state_id)
                     VALUES (%s, %s, %s, %s, %s, %s,
                     %s, %s, %s, %s, %s, %s, %s, %s,
                     %s, %s, %s, %s, %s);""",
                     (
                         row["magnitude"],
                         row["latitude"],
                         row["longitude"],
                         row["time"],
                         row["updated"],
                         row["depth"],
                         row["url"],
                         row["felt"],
                         row["tsunami"],
                         row["cdi"],
                         row["mmi"],
                         row["nst"],
                         row["sig"],
                         row["net"],
                         row["dmin"],
                         row["alert"],
                         row["location_source"],
                         row["magnitude_type"],
                         state_id
                     ))


def upload_df_to_db(conn: Connection, data: DataFrame):
    """Upload DataFrame to database."""
    for _, row in data.iterrows():
        try:
            upload_row_to_db(conn, row.to_dict())
        except (DatabaseError, KeyError, ValueError) as e:
            logger.error("Failed to upload row with id %s: %s",
                         row.get("earthquake_id", "<unknown>"), e)


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
    upload_df_to_db(db_conn, new_quakes)

    return new_quakes


if __name__ == "__main__":
    load_dotenv()
    load_quakes()
