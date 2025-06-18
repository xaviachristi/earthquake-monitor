"""Module for loading pipeline data into a database."""

from os import environ as ENV
from logging import getLogger, basicConfig
from datetime import datetime, timedelta

import pandas as pd
from dotenv import load_dotenv
from psycopg import Connection, connect, rows


logger = getLogger(__name__)

basicConfig(
    level="DEBUG",
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S"
)


def can_be_converted_to_float(string: str) -> bool:
    """Checks if a string can be converted to a float."""
    try:
        float(string)
        return True
    except (ValueError, TypeError):
        return False



def validate_magnitude(magnitude: float) -> bool:
    """Checks if something is a valid magnitude."""
    logger.debug("Validating magnitude: %s", magnitude)

    if not isinstance(magnitude, (float, int)) or isinstance(magnitude, bool):
        raise TypeError(
            f"Magnitude requires a float or int. Received type {type(magnitude)}.")

    if not 0 < magnitude < 11:
        raise ValueError(
            f"Magnitude outside of range (0 to 11). Received {magnitude}.")
    return True


def validate_time(time: str) -> bool:
    """Checks if something is a valid magnitude."""
    logger.debug("Validating time: %s", time)
    if not isinstance(time, str):
        raise TypeError(
            f"Time expected a string. Received type {type(time)}.", )
    try:
        datetime.fromisoformat(time)
    except:
        raise ValueError(
            f"Time should be given in ISO format. E.g. 2025-06-12T00:00:00. Received {time}")
    return True


def validate_api_query_argument_names(arguments: dict) -> bool:
    """
    Are they all valid arguments?
        List of valid arguments, are all the key in there?
        If they have lat, do they have long, vice versa

    Are the values for all the arguments valid?
        Separate functions per argument
    """
    logger.info("Validating arguments: %s", arguments)
    provided_arguments = set(arguments.keys())
    acceptable_arguments = {"lat", "long",
                            "dist", "mag", "start_time", "end_time"}

    if not provided_arguments.issubset(acceptable_arguments):
        logger.error("Unexpected argument. Provided arguments: %s", provided_arguments)
        return False
    if any(provided_arguments) in {"lat", "long", "dist"}:
        logger.error(
            "Searching by lat/long/dist not implemented. Provided arguments: %s",
            provided_arguments)
        raise NotImplementedError("Searching by lat/long/dist not implemented.")

    if "mag" in provided_arguments:
        if isinstance(arguments["mag"], str) \
        and can_be_converted_to_float(arguments["mag"]):
            arguments["mag"] = float(arguments["mag"])
        validate_magnitude(arguments["mag"])

    if "start_time" in provided_arguments:
        validate_time(arguments["start_time"])

    if "end_time" in provided_arguments:
        validate_time(arguments["end_time"])

    if "start_time" in provided_arguments and "end_time" in provided_arguments:
        if arguments["start_time"] > arguments["end_time"]:
            raise ValueError(
                "Start date cannot be after end date."
                f"{arguments["start_time"]}, {arguments["end_time"]}).",)

    return True


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
    logger.info("Preparing query arguments.")
    provided_arguments = arguments.keys()
    prepared_arguments = {}

    if "mag" in provided_arguments:
        prepared_arguments["magnitude"] = arguments["mag"]
    else:
        prepared_arguments["magnitude"] = 4.0

    if "start_time" in provided_arguments:
        prepared_arguments["start_time"] = datetime.fromisoformat(
            arguments["start_time"])
    else:
        prepared_arguments["start_time"] = datetime.now(
        ) - timedelta(days=7)

    if "end_time" in provided_arguments:
        prepared_arguments["end_time"] = datetime.fromisoformat(
            arguments["end_time"])
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
        return None

    logger.debug("Data from database:\n%s",quakes)
    return format_sql_response_as_json(
        quakes.drop(columns=["state_id", "region_id", "state_region_interaction_id"]))


def format_sql_response_as_json(sql_response: pd.DataFrame) -> str:
    """Format the SQL response as the desired JSON."""
    return sql_response.to_dict(orient="records")


if __name__ == "__main__":
    load_dotenv()
    conn = get_connection()
    received_args = {"start_time": "2025-06-17T01:00:00","end_time":"2025-06-17T03:00:00"}
    q = get_query_template()
    sql_args = prepare_query_arguments(received_args)
    print(query_database(conn, q, sql_args))
