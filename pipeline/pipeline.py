"""Script for running full ETL pipeline as AWS lambda."""

from json import dumps
from argparse import ArgumentParser
from datetime import datetime, timedelta
from logging import getLogger, basicConfig
from os import environ as ENV

from pandas import DataFrame
from dotenv import load_dotenv

from extract import extract
from transform import transform
from load import load
from topic import get_topic_dictionaries


logger = getLogger(__name__)

basicConfig(
    level="DEBUG",
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S"
)


def run_pipeline(start: datetime = datetime.now() - timedelta(hours=4),
                 end: datetime = datetime.now()) -> DataFrame:
    """Run ETL pipeline."""
    logger.info(
        "Found environment: %s, %s, %s", ENV["DB_USER"], ENV["DB_HOST"], ENV["DB_NAME"])

    logger.info("Extracting data from API...")
    raw = extract("USGS", "/tmp/temp_earthquake_data.json", start, end)
    if raw is False or not raw or len(raw) == 0:
        logger.warning("No data returned from API.")
        return None

    logger.info("Transforming data...")
    transformed = transform(raw)
    if transformed.empty:
        logger.warning("Failed to transform data returned from API.")
        return None
    logger.info("Transformed data into: %s", transformed)

    logger.info("Loading data to RDS...")
    uploaded = load(transformed)
    if uploaded.empty:
        logger.warning("No data uploaded to RDS.")
        return None
    logger.info("Loaded data into RDS: %s", uploaded)

    return uploaded


def lambda_handler(event, context):
    """
    Main Lambda Handler Function
    Parameters:
        event: Dict containing the lambda function event data
        context: lAMBDA RUNTIME CONTEXT
    Returns:
        Dict containing status message and topics with earthquake values
    """
    try:
        logger.info("Getting time window from event...")
        start_time, end_time = get_time_window_from_event(event)

        logger.info("Running ETL pipeline...")
        data = run_pipeline(start_time,
                            end_time)

        topics = None
        output = None

        if data is not None:
            if not data.empty:
                logger.info("Creating alert dictionary...")
                topics = get_topic_dictionaries(data)
                output_df = data.copy()
                output_df['time'] = output_df['time'].dt.strftime(
                    r"%Y-%m-%d %H:%M")
                output_df['updated'] = output_df['updated'].dt.strftime(
                    r"%Y-%m-%d %H:%M")
                output = output_df["url"].to_list()

        return {
            "statusCode": 200,
            "earthquakes": output,
            "message": topics
        }
    except Exception as e:
        logger.error("Error running pipeline lambda", exc_info=True)
        raise RuntimeError(f"Python pipeline failed to execute: {e}") from e


def get_time_window_from_cli() -> tuple[datetime, datetime]:
    """Get start and end time from runtime arguments for local pipeline."""
    parser = ArgumentParser(description="Process start and end times.")

    parser.add_argument(
        '--start',
        required=True,
        help="Start time in format YYYY-MM-DD HH:MM"
    )

    parser.add_argument(
        '--end',
        '-e',
        required=False,
        help="End time in format YYYY-MM-DD HH:MM"
    )

    args = parser.parse_args()
    return get_datetimes(args.start, args.end)


def get_time_window_from_event(event) -> tuple[datetime, datetime]:
    """
    Get start and end time, in format "%Y-%m-%d %H:%M",
    from runtime event for lambda pipeline.
    """
    start_time = event.get("start")
    end_time = event.get("end", None)
    return get_datetimes(start_time, end_time)


def get_datetimes(start: str, end: str = None):
    """Return datetime tuple from strings."""
    logger.info("Getting datetime from strings...")
    start_time = datetime.strptime(start, "%Y-%m-%d %H:%M")
    if end:
        end_time = datetime.strptime(end, "%Y-%m-%d %H:%M")
    else:
        end_time = datetime.now()

    if start_time >= end_time:
        logger.error("Error: Start time must be before end time.")
    return (start_time, end_time)


if __name__ == "__main__":
    load_dotenv()
    window_start, window_end = get_time_window_from_cli()
    run_pipeline(window_start, window_end)
