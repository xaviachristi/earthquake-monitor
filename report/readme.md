# Reporting

This directory contains the logic for generating daily earthquake summary reports as HTML-styled PDF files. It includes the core script, automated tests, required dependencies, and a wireframe reference image for the report layout.


## Contents
- **`main.py`** — Generates the daily earthquake report as a PDF and uploads it to an AWS S3 bucket.
- **`test_main.py`** — Unit tests for the reporting logic.
- **`requirements.txt`** — Dependencies required to run the reporting script.
- **`report_wireframe.png`** — Visual wireframe of the PDF layout used in the report.

## Setup Instructions
1. **Install Dependencies**  
   Set up a virtual environment and install required Python packages:
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt

##
2. **Configure your environment variables**
DB_HOST=your-db-host
DB_PORT=5432
DB_NAME=your-db-name
DB_USER=your-db-user
DB_PASSWORD=your-db-password
S3_BUCKET=your-s3-bucket-name
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
AWS_REGION=your-region


## PDF Report Logic
- Queries the database for the past 24 hours of earthquake data.
- Summarises and formats the data into a styled PDF.
- The PDF layout is styled using inline HTML/CSS and rendered with xhtml2pdf.
- The generated file is temporarily saved in /tmp/ and automatically uploaded to S3.