"""Script for generating data report."""
from datetime import datetime
from os import environ as ENV
from logging import getLogger
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from os.path import basename
import psycopg2
import pandas as pd
from dotenv import load_dotenv
from pandas import DataFrame
import boto3
from xhtml2pdf import pisa


DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")


def get_db_connection():
    """Get connection."""
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return conn


def fetch_earthquake_data():
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
    total, most_significant, max_mag, active_region, tsunamis = generate_summary(
        df)

    html = f"""
    <html>
    <head><style>body {{ font-family: sans-serif; }}</style></head>
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
            <td>{row['state_name']}</td>
            <td>{row['region_name']}</td>
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
    path = "/tmp/earthquake_report.pdf"
    with open(path, "wb") as output:
        pisa.CreatePDF(html, dest=output)
        return path


def get_email_with_attachment(pdf_path: str) -> str:
    msg = MIMEMultipart('mixed')
    msg['Subject'] = "Daily Earthquake PDF Report"
    msg['From'] = "quakinginmanhattan@hotmail.com"
    msg['To'] = "quakinginmanhattan@hotmail.com"

    body = MIMEText("Attached is your daily earthquake report.", 'plain')
    msg.attach(body)

    with open(pdf_path, 'rb') as f:
        part = MIMEApplication(f.read(), Name=basename(pdf_path))
        part['Content-Disposition'] = f'attachment; filename="{basename(pdf_path)}"'
        msg.attach(part)

    return msg.as_string()


def lambda_handler(event, context):
    """Main lambda handler function."""
    df = fetch_earthquake_data()
    html = generate_html(df)
    pdf_path = get_pdf(html)
    email_string = get_email_with_attachment(pdf_path)
    ses = boto3.client("ses", region_name=os.getenv("AWS_REGION"))
    response = ses.send_raw_email(RawMessage={"Data": email_string})
    return {"status_code": 200,
            "message": "PDF generated and email formatted.",
            "pdf_path": pdf_path,
            "ses_message_id": response.get("MessageId")
            }


if __name__ == "__main__":
    load_dotenv()
    lambda_handler("", "")
