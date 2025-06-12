"""File that turns the notification-making into a lambda."""

from notification_maker import send_emails


def lambda_handler(event: dict, context: dict) -> dict:
    """Creates a lambda handler."""
    status = event.get("status_code")
    if status == 200:
        data = event.get("message")
        send_emails(data)
        return {None: None}
    return {None: None}
