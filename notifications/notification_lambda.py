"""File that turns the notification-making into a lambda."""

from notification_maker import send_emails, get_sns_client


def lambda_handler(event: dict, context: dict) -> dict:
    """Creates a lambda handler."""
    if event.get("message"):
        sns = get_sns_client()
        data = event["message"]
        send_emails(data, sns)
        return {None: None}
    return {None: None}
