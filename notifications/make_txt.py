"""Script to save a HTML so its format can be checked."""

from datetime import datetime

from notification_maker import make_message


def write_to_file(message: str) -> None:
    """Creates a .txt file with sample data."""
    with open("fake_alert.txt", "w", encoding="utf-8") as f:
        f.write(message)


if __name__ == "__main__":

    fake_data = {"topic_arn": "a", "magnitude": 3.1, "state_name": "Not in the USA",
                 "region_name": "Taiwan", "time": datetime.now(), "tsunami": True,
                 "latitude": 30.101, "longitude": 50.123}
    write_to_file(make_message(fake_data))
