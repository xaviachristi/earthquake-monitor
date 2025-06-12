"""Module for loading pipeline data into a database."""

from os import environ as ENV
from logging import getLogger, basicConfig

from dotenv import load_dotenv
from pandas import DataFrame, Series
from psycopg import Connection, connect, rows


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
    return DataFrame.from_dict(quakes).drop(columns=["state_id", "region_id"])


def get_diff(df1: DataFrame, df2: DataFrame) -> DataFrame:
    """Return records that only exist in first DataFrame."""
    df_diff = df1.merge(df2, how='left', indicator=True)
    return df_diff[df_diff['_merge'] == 'left_only'].drop(columns=['_merge'])


def upload_row_to_db(row: Series, conn: Connection):
    """Upload row as Series to database."""
    logger.info("Uploading row with id: %s", row["earthquake_id"])

    logger.info("Uploading region data...")
    with conn.cursor() as curs:
        curs.execute("""INSERT INTO region(region_name)
                     VALUES (%s)
                     RETURNING region_id;""",
                     (row["region_name"],))
        region_id = curs.fetchone()[0]

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
                     %s, %s, %s, %s, %s, %s, %s, %s
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
    data.apply(upload_row_to_db, axis=1, args=(conn,))


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
