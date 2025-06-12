"""Module for displaying reports page."""

from streamlit import (title, html, button,
                       columns, download_button, date_input)
from streamlit_pdf_viewer import pdf_viewer

from report import get_report


def serve_page():
    """Serve Reports page."""
    title("Reports")
    col1, col2 = columns([0.3, 0.7])
    show_report = False
    pdf_bytes = b""

    with col1:
        select_date = date_input(
            label="Select report date.", value="today")
        show_report = button("View Report")
        if show_report:
            pdf_bytes = get_report(select_date)
        download_button("Download Report", pdf_bytes, "report.pdf")
    with col2:
        if show_report:
            pdf_viewer(input=pdf_bytes, annotations=[])
        else:
            html('<p style="text-align: center;">View box for report pdf.</p>')


if __name__ == "__main__":
    serve_page()
