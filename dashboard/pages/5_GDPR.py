"""Module for serving GDPR page."""

from streamlit import (title, markdown,
                       sidebar, image)


def serve_page():
    """Serve GDPR page."""
    title("GDPR")
    with sidebar:
        image("earthquake_monitor.png")
    markdown(
        """
        Our project team will collect your data through the subscription form.
        By submitting the subscription form you are giving your consent for the following:
        - Storing your personal data in our database.
        - Storing preference information and personal information.
        - Personal information will include email address and full name.
        We will use this data to provide you tailored alerts on earthquake activity you are interested.
        """
    )
    markdown(
        """
        When you get an alert, you will always get an option to unsubscribe from that topic.
        This will delete any data we have been holding on you to provide your subscription.
        """
    )


if __name__ == "__main__":
    serve_page()
