"""File that turns the notification-making into a lambda."""

from notification_maker import send_emails


def lambda_handler(event: dict, context: dict) -> dict:
    """Creates a lambda handler."""
    if event.get("message"):
        data = event["message"]
        send_emails(data)
        return {None: None}
    return {None: None}
