"""Script for running full ETL pipeline as AWS lambda."""

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


def run_pipeline(start: datetime = datetime.now() - timedelta(minutes=1),
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
        Dict containing status message
    """
    try:
        logger.info("Running ETL pipeline...")
        data = run_pipeline(datetime.now() - timedelta(hours=24),
                            datetime.now())

        topics = None

        if data is not None:
            if not data.empty:
                logger.info("Creating alert dictionary...")
                topics = get_topic_dictionaries(data)

        return {
            "statusCode": 200,
            "message": topics
        }
    except Exception as e:
        logger.error("Error running pipeline lambda", exc_info=True)
        raise RuntimeError(f"Python pipeline failed to execute: {e}") from e


if __name__ == "__main__":
    load_dotenv()
    run_pipeline(datetime.now() - timedelta(hours=24),
                 datetime.now())
