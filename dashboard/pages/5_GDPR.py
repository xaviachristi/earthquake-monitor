"""Module for serving GDPR page."""

from streamlit import (title, sidebar, markdown, 
                       columns, button)

from subscription import view_subscription, delete_subscription

def serve_page():
    """Serve GDPR page"""
    title("GDPR")
    sidebar.header("GDPR")
    markdown(
        """
        Our project team will collect your data through the subscription form.
        By submitting the subscription form you are giving your consent for the following:
        - Store your personal data in our database.
        - Store preference information and personal information.
        - Personal information will include email address and full name.
        We will use this data to provide you tailored alerts on earthquake activity you are interested.
        """
    )
    col1, col2, _, _ = columns(4)
    with col1:
        button("View my personal data", on_click=view_subscription)
    with col2:
        button("Remove my personal data", on_click=delete_subscription)


if __name__ == "__main__":
    serve_page()
