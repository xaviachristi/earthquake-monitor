import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
import psycopg2
from main import generate_summary, generate_html, get_pdf


@pytest.fixture
def sample_dataframe():
    return pd.DataFrame([
        {
            'time': pd.Timestamp('2025-06-17 07:36'),
            'state_name': 'California',
            'region_name': 'West Coast',
            'magnitude': 5.3,
            'depth': 10.0,
            'felt': 20,
            'url': 'http://example.com',
            'tsunami': 0,
            'sig': 600
        },
        {
            'time': pd.Timestamp('2025-06-17 06:00'),
            'state_name': 'Nevada',
            'region_name': 'West Coast',
            'magnitude': 4.8,
            'depth': 12.5,
            'felt': 5,
            'url': 'http://example.com/2',
            'tsunami': 0,
            'sig': 400
        }
    ])


def test_generate_summary_with_data(sample_dataframe):
    total, most_significant, largest_mag, most_active, tsunami_count = generate_summary(
        sample_dataframe)

    assert total == 2
    assert "Magnitude 5.3" in most_significant
    assert largest_mag == 5.3
    assert most_active == "West Coast"
    assert tsunami_count == 0


def test_generate_summary_empty():
    empty_df = pd.DataFrame()
    total, most_significant, largest_mag, most_active, tsunami_count = generate_summary(
        empty_df)

    assert total == 0
    assert most_significant == "No earthquake data available."
    assert largest_mag == 0
    assert most_active == "N/A"
    assert tsunami_count == 0


def test_generate_html(sample_dataframe):
    html = generate_html(sample_dataframe)
    assert "<html>" in html
    assert "Earthquake Report" in html
    assert "Top 3 Earthquakes" in html
    assert "California" in html


@patch("main.pisa.CreatePDF")
def test_get_pdf(mock_pisa):
    mock_pisa.return_value = (MagicMock(), True)
    html = "<html><body><p>Test</p></body></html>"
    path, filename = get_pdf(html)

    assert path.startswith("/tmp/earthquake_report_")
    assert filename.endswith(".pdf")
    mock_pisa.assert_called_once()


@patch("main.boto3.client")
def test_upload_to_s3(mock_boto):
    mock_s3 = MagicMock()
    mock_boto.return_value = mock_s3

    from main import S3_BUCKET, upload_to_s3
    fake_path = "/tmp/fake.pdf"
    result = upload_to_s3(fake_path)

    assert result.startswith(f"https://{S3_BUCKET}.s3.amazonaws.com/reports/")
    mock_s3.upload_file.assert_called_once()
