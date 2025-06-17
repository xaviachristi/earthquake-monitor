"""Module for loading pipeline data into a database."""

from os import environ as ENV
from logging import getLogger, basicConfig
from datetime import datetime
from pytz import timezone

from dotenv import load_dotenv
from pandas import DataFrame, to_numeric
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
        port=ENV["DB_PORT"],
        password=ENV["DB_PASSWORD"],
        row_factory=rows.dict_row
    )


def get_current_db() -> DataFrame:
    """Return all records currently in database."""
    logger.info("Getting database connection...")
    conn = get_connection()

    with conn.cursor() as curs:
        curs.execute("""SELECT * FROM earthquake
                        JOIN "state_region_interaction" USING(state_region_interaction_id)
                        JOIN "state" USING (state_id)
                        JOIN "region" USING (region_id);""")
        quakes = DataFrame(curs.fetchall())
    if quakes.empty:
        quake_cols = [
            "earthquake_id", "magnitude", "latitude", "longitude", "time", "updated",
            "depth", "url", "felt", "tsunami", "cdi", "mmi", "nst", "sig", "net", "dmin",
            "alert", "location_source", "magnitude_type", "state_name", "region_name",
            "state_id", "region_id"
        ]
        return DataFrame(columns=quake_cols)
    return quakes.drop(columns=["state_id", "region_id"])


def preprocess_df(df: DataFrame) -> DataFrame:
    """Returned sanitised dfs for merging."""
    numeric_cols = ['latitude', 'longitude',
                    'magnitude', 'depth', 'cdi', 'mmi', 'dmin']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = to_numeric(df[col], errors='coerce')

    london_tz = timezone("Europe/London")
    df["time"] = df["time"].apply(
        lambda ts: london_tz.localize(datetime.fromtimestamp(ts/1000)))
    df["updated"] = df["updated"].apply(
        lambda ts: london_tz.localize(datetime.fromtimestamp(ts/1000)))

    df['latitude'] = df['latitude']
    df['longitude'] = df['longitude']
    df['magnitude'] = df['magnitude']
    df['depth'] = df['depth']
    df['cdi'] = df['cdi']
    df['mmi'] = df['mmi']
    df['dmin'] = df['dmin']
    df["tsunami"] = df["tsunami"].apply(lambda x: bool(x))
    df["magnitude_type"] = df["magnitude_type"].str.title()
    df['felt'] = df['felt'].fillna(0).astype(int)
    df['felt'] = df['felt'].apply(lambda x: int(x))

    return df


def get_diff(df1: DataFrame, df2: DataFrame) -> DataFrame:
    """Return records that only exist in first DataFrame."""
    df1 = preprocess_df(df1)

    df1 = df1.drop(columns=["earthquake_id", "location_source"])

    df1 = df1.reset_index(drop=True)

    return df1[~df1["url"].isin(df2["url"])]


def get_region_id(conn: Connection, region: str) -> int | None:
    """Return id of region if it is in the database."""
    logger.info("Checking if region, %s, is in database...", region)
    with conn.cursor() as curs:
        curs.execute("""SELECT * FROM region
                     WHERE region_name ILIKE %s;""",
                     (region,))
        result = curs.fetchone()
    if result:
        logger.debug("Found region: %s", result)
        return result["region_id"]
    return None


def get_state_id(conn: Connection, state: str) -> int | None:
    """Return id of state if it is in the database."""
    logger.info("Checking if state, %s, is in database...", state)
    with conn.cursor() as curs:
        curs.execute("""SELECT * FROM "state"
                     WHERE state_name ILIKE %s;""",
                     (state,))
        result = curs.fetchone()
    if result:
        logger.debug("Found state: %s", result)
        return result["state_id"]
    return None


def get_state_region_id(conn: Connection, state: int, region: int) -> int | None:
    """Return id of state region interaction if it is in the database."""
    logger.info(
        "Checking if state region interaction, %s and %s, is in database...", state, region)
    with conn.cursor() as curs:
        curs.execute("""SELECT * FROM "state_region_interaction"
                     WHERE state_id = %s
                     AND region_id = %s;""",
                     (state, region))
        result = curs.fetchone()
    if result:
        logger.debug("Found state region interaction: %s", result)
        return result["state_region_interaction_id"]
    return None


def upload_row_to_db(row: dict):
    """Upload row as a dictionary to the database."""

    logger.info("Getting database connection...")
    conn = get_connection()

    logger.debug("Uploading row: %s", row)

    region_id = get_region_id(conn, row["region_name"])

    if region_id is None:
        logger.info("Uploading region data...")
        with conn.cursor() as curs:
            curs.execute("""INSERT INTO region(region_name)
                        VALUES (%s)
                        RETURNING region_id;""",
                         (row["region_name"],))
            region_id = curs.fetchone()["region_id"]

    state_id = get_state_id(conn, row["state_name"])

    if state_id is None:
        logger.info("Uploading state data...")
        with conn.cursor() as curs:
            curs.execute("""INSERT INTO state(state_name, region_id)
                        VALUES (%s, %s)
                        RETURNING state_id;""",
                         (row["state_name"], region_id))
            state_id = curs.fetchone()["state_id"]

    state_region_id = get_state_region_id(conn, state_id, region_id)

    if state_region_id is None:
        logger.info("Uploading state region interaction...")
        with conn.cursor() as curs:
            curs.execute("""INSERT INTO state_region_interaction(state_id, region_id)
                        VALUES (%s, %s)
                        RETURNING state_region_interaction_id;""",
                         (state_id, region_id))
            state_region_id = curs.fetchone()["state_region_interaction_id"]

    logger.info("Uploading earthquake data...")
    with conn.cursor() as curs:
        curs.execute("""INSERT INTO earthquake(magnitude,
                     latitude, longitude, "time", updated, depth,
                     "url", felt, tsunami, cdi, mmi, nst,
                     sig, net, dmin, alert,
                     magnitude_type, state_region_interaction_id)
                     VALUES (%s, %s, %s, %s, %s, %s,
                     %s, %s, %s, %s, %s, %s, %s, %s,
                     %s, %s, %s, %s);""",
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
                         row["magnitude_type"],
                         state_region_id
                     ))
        conn.commit()


def upload_df_to_db(data: DataFrame):
    """Upload DataFrame to database."""
    for _, row in data.iterrows():
        try:
            upload_row_to_db(row.to_dict())
        except (DatabaseError, KeyError, ValueError) as e:
            logger.error("Failed to upload row: %s", e)


def load(quakes: DataFrame) -> DataFrame:
    """Return earthquakes that have been uploaded to the database."""
    logger.info("Getting data already in database...")
    old_quakes = get_current_db()
    if not old_quakes.empty:
        logger.debug("Found old earthquake data: \n%s", old_quakes.head())
    else:
        logger.debug("No old earthquake data found.")

    logger.info("Identifying new earthquake data...")
    new_quakes = get_diff(quakes, old_quakes)
    if not new_quakes.empty:
        logger.debug("Found new earthquake data: \n%s", new_quakes.head())

        logger.info("Uploading new data to database...")
        upload_df_to_db(new_quakes)
    else:
        logger.debug("No new earthquake data found.")

    logger.info("Load run successful.")
    return new_quakes


if __name__ == "__main__":
    london_tz = timezone("Europe/London")
    sample_df = DataFrame([
        {
            "earthquake_id": 1,
            "magnitude": 2.5,
            "latitude": 10.0,
            "longitude": 20.0,
            "time": london_tz.localize(datetime.strptime("2024-02-01", "%Y-%m-%d")),
            "updated": london_tz.localize(datetime.strptime("2024-02-02", "%Y-%m-%d")),
            "depth": 5.0,
            "url": "example.com/1",
            "felt": 1,
            "tsunami": False,
            "cdi": 3.1,
            "mmi": 2.3,
            "nst": 1,
            "sig": 1,
            "net": "us",
            "dmin": 0.1,
            "alert": "green",
            "location_source": "us",
            "magnitude_type": "Mb",
            "state_name": "California",
            "region_name": "West Coast",
            "state_id": 12,
            "region_id": 4
        },
        {
            "earthquake_id": 2,
            "magnitude": 3.7,
            "latitude": 11.0,
            "longitude": 21.0,
            "time": london_tz.localize(datetime.strptime("2024-02-01", "%Y-%m-%d")),
            "updated": london_tz.localize(datetime.strptime("2024-02-02", "%Y-%m-%d")),
            "depth": 7.0,
            "url": "example.com/2",
            "felt": 0,
            "tsunami": True,
            "cdi": 2.8,
            "mmi": 2.1,
            "nst": 2,
            "sig": 2,
            "net": "us",
            "dmin": 0.2,
            "alert": "yellow",
            "location_source": "us",
            "magnitude_type": "Mb",
            "state_name": "Nevada",
            "region_name": "Southwest",
            "state_id": 13,
            "region_id": 4
        }
    ])
    load_dotenv()
    load(sample_df)
