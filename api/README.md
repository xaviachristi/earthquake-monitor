# API

- This directory contains all the necessary files to run the project's API.
- Further information on the API is contained in `static/documentation.html` - which is also served as the index page of the API.
- All commands in this document should be ran from this directory `~/<path-to-directory>`

# Setup

- Create a venv.
    - `python -m venv .venv`
- Install dependencies.
    - `pip install -r requirements.txt`
- Create an environment file called `.env`.
    - Template `.env` file:
        ```
        DB_HOST=[host address]
        DB_USER=[username]
        DB_NAME=[database name]
        DB_PORT=[database port]
        DB_PASSWORD=[password]
        ```
    - Example `.env` file:
        ```
        DB_HOST=127.0.0.1
        DB_USER=postgres
        DB_NAME=earthquake_db
        DB_PORT=5432
        DB_PASSWORD= # Left blank as no pw
        ```
- Run the API.
    - `python app.py`


# Scripts

- `app.py` contains and runs the endpoints for the API.

# Modules

- `app_functions.py` functions to validate and format the arguments passed into the API.

# Testing

- All the python utilty modules have associated test files in the format `test_<module_name>.py`.
- `conftest.py` provides test fixtures for those tests.
- To run the test suite
    - `pytest *.py`
    - or
    - `pytes *.py -vvx` for more information.
