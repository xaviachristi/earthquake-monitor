"""Script for running full ETL pipeline as AWS lambda."""

from logging import getLogger, basicConfig
from os import environ as ENV

from pandas import DataFrame

from extract import extract
from transform import transform
from load import load


logger = getLogger(__name__)

basicConfig(
    level="DEBUG",
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S"
)


def get_topic_dictionaries(data: DataFrame) -> dict:
    """Return topic strings and value list for sending alerts."""


def run_pipeline() -> dict:
    """Run ETL pipeline."""
    logger.info(
        "Found environment: %s, %s", ENV["DB_USER"], ENV["DB_HOST"], ENV["DB_NAME"])

    logger.info("Extracting data from API...")
    raw = extract()

    logger.info("Transforming data...")
    transformed = transform(raw)

    logger.info("Loading data to RDS...")
    uploaded = load(transformed)

    return uploaded


def lambda_handler(event, context):
    """
    Main Lambda Handler Function
    Parameters:
        event: Dict containing the lambda function event data
        context: lAMBDA RUNTIME CONTEXT
    Returns:
        Dict containing status message
    """
    try:
        logger.info("Running ETL pipeline...")
        data = run_pipeline()

        logger.info("Creating alert dictionary...")
        topics = get_topic_dictionaries(data)

        return {
            "statusCode": 200,
            "message": topics
        }
    except Exception as e:
        logger.error("Error running pipeline lambda: %s", str(e))
        raise RuntimeError("Python pipeline failed to execute: %s", e)
