"""API for accessing earthquake data."""
"""
Planning:

From Issue:
    Multiple endpoints
    Filters
        region
        lat/long
        date
        mag
    Get requests only

API Script:
    Flask
    Returns JSON
    Port 80
    Endpoints:
        - URL/earthquakes?region=____&lat=___&long=___&date=____&mag=___
          (THE MAIN ONE)
        - Most recent earthquake
        - Biggest earthquake in the past 24 hours
    Might be nice to add a state filter as well
    Remember logging!
    Documentation important
    SQL Queries should be easy -> look at dashboard script for reference
    Should handle incorrect API queries gracefully
    RESTful!
    FastAPI vs Flask? -> Flask - more reliable, we don't need any of the features
                         of FastAPI really.
    Can start with the

    General flow:
    - One API endpoint with many filters
    - Constructs SQL query
    - Uses SQL query
    - Formats data as an appropriate JSON
    - returns this json

    - Depending on the result of the SQL query, change status code
    
"""
from os import environ as ENV
from logging import getLogger, basicConfig

from dotenv import load_dotenv
from flask import Flask, current_app, request

from api_functions import (validate_api_query_argument_names, prepare_query_arguments,
                           get_connection, get_query_template, format_sql_response_as_json,
                           query_database)


logger = getLogger(__name__)
basicConfig(
    level="DEBUG",
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S"
)


APP = Flask(__name__)

CONN = get_connection()


@APP.get("/")
@APP.get("/home")
def index():
    """Returns documentation for the API."""
    logger.debug("Index accessed.")
    return current_app.send_static_file("documentation.html")


@APP.get("/earthquakes")
def get_earthquakes():
    """
    Main endpoint for the API.
    Currently allows for filtering by magnitude and time.
    See documentation.html for more information.
    """
    logger.info("Request received.")
    args = request.args.to_dict()

    try:
        validate_api_query_argument_names(args)

    except ValueError as e:
        logger.error("Value error: %s", str(e))
        return {"error": True,
                "content": str(e)}, 400

    except TypeError as e:
        logger.error("Type error: %s", str(e))
        return {"error": True,
                "content": str(e)}, 400

    q = get_query_template()
    sql_args = prepare_query_arguments(args)
    # fillna being depreciated - easiest way to replace it?
    res = query_database(CONN, q, sql_args)

    if res:
        return {"error": False,
            "content": res}, 200
    else:
        return {"error": False,
            "content": res}, 204


if __name__ == "__main__":
    load_dotenv()
    APP.config['TESTING'] = True
    APP.config['DEBUG'] = True
    APP.run(debug=True, host="0.0.0.0", port=80)
