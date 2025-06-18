"""Script for generating data report."""
from datetime import datetime
from os import environ as ENV
from os.path import basename
import os
import psycopg2
import pandas as pd
from dotenv import load_dotenv
from pandas import DataFrame
import boto3
from xhtml2pdf import pisa

load_dotenv()


DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
S3_BUCKET = os.getenv("S3_BUCKET")


def get_db_connection():
    """Get connection to database."""
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return conn


def fetch_earthquake_data():
    "Retrieve earthquake data from external USGS API."
    conn = get_db_connection()
    query = """SELECT
                    e.*,
                    s.state_name,
                    r.region_name
                FROM earthquake e
                JOIN state_region_interaction sri ON e.state_region_interaction_id = sri.state_region_interaction_id
                JOIN state s ON sri.state_id = s.state_id
                JOIN region r ON sri.region_id = r.region_id
                WHERE e.time >= NOW() - INTERVAL '1 day';
            """
    df = pd.read_sql(query, conn)
    conn.close()
    return df


def generate_summary(df: DataFrame):
    """Return summary of data from Dataframe."""
    total = len(df)

    if df.empty:
        most_significant = "No earthquake data available."
        largest_mag = 0
        most_active = "N/A"
        tsunami_count = 0
    else:
        most_significant_row = df.sort_values(
            by='sig', ascending=False).iloc[0]
        most_significant = (
            f"Magnitude {most_significant_row['magnitude']} in {most_significant_row['state_name']}, "
            f"{most_significant_row['region_name']} on {most_significant_row['time'].strftime('%Y-%m-%d %H:%M')}, "
            f"Felt by {most_significant_row['felt'] or 0}, Tsunami: {'Yes' if most_significant_row['tsunami'] else 'No'}"
        )
        largest_mag = df['magnitude'].max()
        most_active = df['region_name'].value_counts(
        ).idxmax()
        tsunami_count = df[df['tsunami'] == 1].shape[0]
    return total, most_significant, largest_mag, most_active, tsunami_count


def generate_html(df: DataFrame) -> str:
    "Put retrieved data values into formatted pdf report."
    total, most_significant, max_mag, active_region, tsunamis = generate_summary(
        df)

    html = f"""
    <html>
    <head><style>html, body {{
                margin: 0;
                padding: 0;
                background-color: #efeae1;
                font-family: Georgia, serif;
                color: #6f2022;
            }}
            .container {{
                padding: 30px;
                background-color: #efeae1;
            }}
            h1 {{
                text-align: center;
                margin-bottom: 20px;
                color: #6f2022;
            }}
            h2, h3 {{
                margin-top: 30px;
                color: #6f2022;
            }}
            ul {{
                padding-left: 20px;
                line-height: 1.6;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }}
            th {{
                background-color: #425953;
                color: white;
                padding: 8px;
                border: 1px solid #583b3d;
            }}
            td {{
                background-color: #ffffff;
                color: #000000;
                padding: 6px;
                border: 1px solid #cccccc;
                text-align: center;
            }}
            a {{
                color: #6f2022;
                text-decoration: none;
                font-weight: bold;
            }}
    </style></head>
    <body>
        <h1>[{datetime.now().strftime('%Y-%m-%d')}] Earthquake Report</h1>

        <h2>Summary Metrics</h2>
        <ul>
            <li>Total earthquakes: {total}</li>
            <li>Most significant earthquake: {most_significant}</li>
            <li>Largest magnitude: {max_mag}</li>
            <li>Most active region: {active_region}</li>
            <li>Number of tsunamis: {tsunamis}</li>
        </ul>

        <h3>Top 3 Earthquakes by Magnitude</h3>
        <table border="1" cellpadding="5">
            <tr><th>Time</th><th>Location</th><th>Mag</th><th>Depth</th><th>Felt?</th><th>URL</th><th>Tsunami</th></tr>
    """
    top_mag = df.sort_values(by='magnitude', ascending=False).head(3)
    for _, row in top_mag.iterrows():
        html += f"""
        <tr>
            <td>{row['time'].strftime('%H:%M')}</td>
            <td>{row['state_name']}, {row['region_name']}</td>
            <td>{row['magnitude']}</td>
            <td>{row['depth']}</td>
            <td>{'Yes' if row['felt'] and row['felt'] > 0 else 'No'}</td>
            <td><a href='{row['url']}'>Link</a></td>
            <td>{'Yes' if row['tsunami'] else 'No'}</td>
        </tr>
        """
    html += "</table></body></html>"
    return html


def get_pdf(html: str) -> str:
    "Names pdf file with datetime."
    filename = f"earthquake_report_{datetime.now().strftime('%Y%m%d')}.pdf"
    path = f"/tmp/{filename}"
    with open(path, "wb") as output:
        pisa.CreatePDF(html, dest=output)
    return path, filename


def upload_to_s3(pdf_path: str) -> str:
    """Upload PDF to S3 and return its URL."""
    s3 = boto3.client('s3')

    object_name = f"reports/earthquake_report_{datetime.now().strftime('%Y-%m-%d')}.pdf"
    s3.upload_file(pdf_path, S3_BUCKET, object_name, ExtraArgs={
                   'ContentType': 'application/pdf'})
    url = f"https://{S3_BUCKET}.s3.amazonaws.com/{object_name}"
    return url


def lambda_handler(event, context):
    """Main lambda handler function."""
    df = fetch_earthquake_data()
    html = generate_html(df)
    pdf_path, filename = get_pdf(html)
    download_url = upload_to_s3(pdf_path)
    return {
        "statusCode": 200,
        "message": "PDF generated and uploaded to S3.",
        "download_url": download_url
    }


if __name__ == "__main__":
    lambda_handler("", "")
