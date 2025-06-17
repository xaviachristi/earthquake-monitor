"""Module for displaying the subscribe page."""

from streamlit import (title, markdown, button,
                       columns, text_input, number_input,
                       slider)

from subscription import make_subscription


def serve_page():
    """Serve Subscribe page."""
    title("Subscribe")
    col1, col2 = columns([0.43, 0.7])
    with col1:
        email = text_input(
            "Email Address", placeholder="johnsmith@earthquakes.net")
        latitude = number_input(
            "Latitude", min_value=-90.0, max_value=90.0, value=0.0)
        longitude = number_input("Longitude", min_value=-
                                 180.0, max_value=180.0, value=0.0)
        radius = slider("Radius of Search / km", min_value=0,
                        value=10, max_value=1000)
        magnitude = number_input(
            "Minimum Magnitude", min_value=0.0, max_value=10.0, value="min", format="%0.1f")
        subscribe = button("Subscribe to Alerts")
        if subscribe:
            make_subscription(email, latitude, longitude, radius, magnitude)
    with col2:
        markdown("""This is a subscription form for our alert service.
                 The form requires an email address to send alerts to.
                 As a user you can subscribe to events based on point location
                 and radius in km from that point and/or by magnitude of the event.
                 A user could, for example, target a 100km radius
                 around their house for events of magnitude 4 or greater.
                 """)


if __name__ == "__main__":
    serve_page()
