# Dashboard

- Serves a streamlit dashboard for the project users to interact with the earthquake data.
- All commands in this document should be ran from this directory `~/dashboard`

# Setup

- Create a venv
    - `python -m venv .venv`
- Install dependencies
    - `pip install -r requirements.txt`

## `.env file`
```txt
DB_HOST=<DB_IP_ADDRESS>
DB_PORT=<PORT>
DB_NAME=<NAME_OF_DB>
DB_PASSWORD=<PASS_FOR_DB>
DB_USER=<USER_FOR_ACCESSING_DB>

AWS_DEFAULT_REGION=<AWS_REGION>
AWS_ACCESS_KEY=<AWS_ACCESS_KEY_ID>
AWS_SECRET_ACCESS_KEY=<AWS_SECRET_ACCESS_KEY>
AWS_S3_BUCKET=<S3_BUCKET_NAME>
```

# Serving

- To serve the dashboard locally run this command:
    - `streamlit run Home.py`
- The dashboard will be avaiable at:
    - `localhost:8501`

# Pages

## `Home`

- Landing page for dashboard.
- Contains basic visualisations and information for using the dashboard.

## `USA`

- Serves a USA data page.
- Contains important visualisations and filters.

## `International`

- Serves an International data page.
- Contains important visualisations and filters.

## `Subscribe`

- Serves a page for making a subscription.

## `Reports`

- Serves a page for viewing and downloading reports.

## `GDPR`

- Serves a page of text containing GDPR information for the user.

# Modules

## `Subscription`

- Provides methods for creating subscriptions.

## `Report`
Provides methods for showing and downloading reports stored in S3.
Retrieves the PDF report for a given date from your configured S3 bucket.
Parses and loads the file as raw bytes so it can be rendered or downloaded in the dashboard.

### 🔧 Functions

#### `get_client() -> boto3.client`
Returns an S3 client using environment variables configured in `.env` file:

- `AWS_S3_BUCKET`
- `AWS_ACCESS_KEY`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_DEFAULT_REGION`

#### `get_report(target: date = None) -> bytes`
Fetches the earthquake report (PDF) for the given date from your S3 bucket.

**Parameters:**
- `target` (`datetime.date`, optional): The date for which the report should be fetched. If not provided, returns an empty byte string.

**Returns:**
- `bytes`: The content of the report PDF file as a byte string, or `b""` if no matching report is found.

- The function uses `@streamlit.cache_resource` to cache results and avoid redundant S3 calls.


## `Data`

- Provides methods for pulling data from the database.
- Provides methods for manipulating the data.

## `Charts`

- Provides chart creation methods that are served by dashboard pages.

# Testing

- All the python utilty modules have associated test files in the format `test_<module_name>.py`.
- `conftest.py` provides test fixtures for those tests.
- To run the test suite:
    - `pytest *.py`
    - OR
    - `pytes *.py -vvx` for more information.
