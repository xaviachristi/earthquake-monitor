"""Module for loading pipeline data into a database."""

from os import environ as ENV
from logging import getLogger, basicConfig
from datetime import datetime, timedelta

import pandas as pd
from dotenv import load_dotenv
from psycopg import Connection, connect, rows, DatabaseError


logger = getLogger(__name__)

basicConfig(
    level="DEBUG",
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S"
)


def validate_magnitude(magnitude: float) -> bool:
    """Checks if something is a valid magnitude."""
    if not isinstance(magnitude, (float, int)):
        raise TypeError("Magnitude requires a float or int. Received type %s.", type(magnitude))
    if not -2 < magnitude < 11:
        raise ValueError("Magnitude outside of range (-2 to 11). Received %s.", magnitude)
    return True


def validate_time(time: str) -> bool:
    """Checks if something is a valid magnitude."""
    if not isinstance(time, str):
        raise TypeError(
            "Expected a string formatted as 'YYYY-MM-DDThh-mm-ss'. Received type %s.", type(time))
    try:
        datetime.strptime(time, "YYYY-MM-DDThh-mm-ss")
    except:
        raise ValueError(
            "Expected a string formatted as 'YYYY-MM-DDThh-mm-ss'. Received %s", time)
    return True


def validate_api_query_argument_names(arguments: dict) -> bool:
    """
    Are they all valid arguments?
        List of valid arguments, are all the key in there?
        If they have lat, do they have long, vice versa

    Are the values for all the arguments valid?
        Separate functions per argument
    """
    provided_arguments = set(arguments.keys())
    acceptable_arguments = {"lat", "long",
                            "dist", "mag", "start_time", "end_time"}
    if not provided_arguments.issubset(acceptable_arguments):
        return False
    if any(provided_arguments) in {"lat", "long", "dist"}:
        raise NotImplementedError("Searching by lat/long/dist not implemented.")

    if "mag" in provided_arguments:
        validate_magnitude(arguments["mag"])

    if "start_time" in provided_arguments:
        validate_time(arguments["start_time"])

    if "end_time" in provided_arguments:
        validate_time(arguments["end_time"])

    if "start_time" in provided_arguments and "end_time" in provided_arguments:
        if arguments["start_time"] > arguments["end_time"]:
            raise ValueError("Start date cannot be after end date. ([%s], [%s]).", 
                             arguments["start_time"], arguments["end_time"])

    return True


def get_haversine_distance_formula_in_sql():
    """
    Copy over from pipeline.py
    Will I have to implement this in SQL?
    """
    # SELECT id, (3959 * acos(cos(radians(Lat1)) * cos(radians(Lat2))
    # * cos(radians(Lng2) - radians(Lng1)) + sin(radians(Lat1))
    # * sin(radians(Lat2)))) AS distance
    # FROM     markers
    # HAVING distance < 25
    # ORDER BY distance
    # LIMIT 0, 20
    pass


def get_query_template() -> str:
    """Returns a query to be formatted with %s formatting."""
    return """
        SELECT * FROM earthquake
        JOIN "state_region_interaction" USING(state_region_interaction_id)
        JOIN "state" USING (state_id)
        JOIN "region" USING (region_id)
        WHERE magnitude > %(magnitude)s
        AND time BETWEEN %(start_time)s AND %(end_time)s;
        """


def prepare_query_arguments(arguments: dict) -> str:
    """
    Creates a dictionary of arguments for querying the database.
    Provides defaults and the correct formatting.
    """

    # lat/long/dist can raise a not-implemented error for now
    # as they might need haversine distance
    # I'll do the easier API bits then circle back depending on time.

    provided_arguments = arguments.keys()
    prepared_arguments = {}

    if "mag" in provided_arguments:
        prepared_arguments["magnitude"] = arguments["mag"]
    else:
        prepared_arguments["magnitude"] = 4.0

    if "start_time" in provided_arguments:
        prepared_arguments["start_time"] = datetime.strptime(
            arguments["time"], "YYYY-MM-DDThh-mm-ss")
    else:
        prepared_arguments["start_time"] = datetime.now(
        ) - timedelta(days=7)

    if "end_time" in provided_arguments:
        prepared_arguments["end_time"] = datetime.strptime(
            arguments["end_time"], "YYYY-MM-DDThh-mm-ss")
    else:
        prepared_arguments["end_time"] = datetime.now()

    return prepared_arguments


def get_connection() -> Connection:
    """Return connection to database."""
    logger.info("Connecting to the database.")
    return connect(
        host=ENV["DB_HOST"],
        user=ENV["DB_USER"],
        dbname=ENV["DB_NAME"],
        port=ENV["DB_PORT"],
        password=ENV["DB_PASSWORD"],
        row_factory=rows.dict_row
    )


def query_database(connection: Connection, query: str, parameters: dict) -> pd.DataFrame:
    """Sends a query to the database."""
    with connection.cursor() as curs:
        curs.execute(query, parameters)
        quakes = pd.DataFrame(curs.fetchall())
    if quakes.empty:
        quake_cols = [
            "earthquake_id", "magnitude", "latitude", "longitude", "time", "updated",
            "depth", "url", "felt", "tsunami", "cdi", "mmi", "nst", "sig", "net", "dmin",
            "alert", "location_source", "magnitude_type", "state_name", "region_name",
            "state_id", "region_id"
        ]
        return pd.DataFrame(columns=quake_cols)
    return quakes.drop(columns=["state_id", "region_id", "state_region_interaction_id"])


def format_sql_response_as_json(sql_response: pd.DataFrame) -> str:
    """Format the SQL response as the desired JSON."""
    return sql_response.to_json(orient="table")


if __name__ == "__main__":
    load_dotenv()
    conn = get_connection()
    received_args = {}
    q = get_query_template()
    sql_args = prepare_query_arguments(received_args)
    # fillna being depreciated - easiest way to replace it?
    print(format_sql_response_as_json(query_database(conn, q, sql_args).fillna(0)))
