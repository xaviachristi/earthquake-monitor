# Dashboard

- Serves a streamlit dashboard for the project users to interact with the earthquake data.
- All commands in this document should be ran from this directory `~/dashboard`

# Setup

<!-- Example for python directories.-->
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
```

# Serving

- To serve the dashboard locally run this command:
    - `streamlit run Home.py`
- The dashboard will be avaiable at:
    - `localhost:8501`

# Pages

## `Home`

- <!-- Module description. -->
- <!-- Key function signiatures. -->

## `Historic`

- <!-- Module description. -->
- <!-- Key function signiatures. -->

## `Recent`

- <!-- Module description. -->
- <!-- Key function signiatures. -->

## `Subscribe`

- <!-- Module description. -->
- <!-- Key function signiatures. -->

## `Reports`

- <!-- Module description. -->
- <!-- Key function signiatures. -->

## `GDPR`

- <!-- Module description. -->
- <!-- Key function signiatures. -->

# Modules

## `Subscription`

- <!-- Module description. -->
- <!-- Key function signiatures. -->

## `Report`

- <!-- Module description. -->
- <!-- Key function signiatures. -->

## `Data`

- <!-- Module description. -->
- <!-- Key function signiatures. -->

## `Charts`

- <!-- Module description. -->
- <!-- Key function signiatures. -->

## `Subscription`

- <!-- Module description. -->
- <!-- Key function signiatures. -->

# Testing

- All the python utilty modules have associated test files in the format `test_<module_name>.py`
- <!-- Include the conftest line if it has been used. -->
- `conftest.py` provides test fixtures for those tests
- To run the test suite
    - `pytest *.py`
    - OR
    - `pytes *.py -vvx` for more information.
