"""API for accessing earthquake data."""
from logging import getLogger, basicConfig

from dotenv import load_dotenv
from flask import Flask, current_app, request

from app_functions import (validate_api_query_argument_names, prepare_query_arguments,
                           get_connection, get_query_template, query_database)


logger = getLogger(__name__)
basicConfig(
    level="DEBUG",
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S"
)


load_dotenv()
app = Flask(__name__)



@app.get("/")
@app.get("/index")
def index():
    """Returns documentation for the API."""
    logger.debug("Index accessed.")
    return current_app.send_static_file("documentation.html")


@app.get("/earthquakes")
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
    res = query_database(CONN, q, sql_args)

    if res:
        return {"error": False,
            "content": res}, 200

    return {"error": False,
        "content": []}, 204
    # 204 could do with better user feedback.
    # Can it redirect to a page describing what has happened?


if __name__ == "__main__":
    CONN = get_connection()
    app.run(debug=True, host="0.0.0.0", port=80)
