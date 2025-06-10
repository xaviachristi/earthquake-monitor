# Pipeline

- <!-- Purpose of directory. -->
- All commands in this document should be ran from this directory `~/<path-to-directory>`

# Installation

- <!-- Neccessary installation instructions. -->
- <!-- Include commands for CLI. -->
- <!-- Include variations for operating system e.g. Mac, Windows, Linux. -->

# `.env file`
- <!-- Example env file below. -->
```txt
DB_HOST=<DB_IP_ADDRESS>
DB_PORT=<PORT>
DB_NAME=<NAME_OF_DB>
DB_PASSWORD=<PASS_FOR_DB>
DB_USER=<USER_FOR_ACCESSING_DB>

AWS_REGION=<REGION_THAT_RESOURCES_DEPLOY_TO>
AWS_ACCESS_KEY_ID=<AWS_USER_KEY_IDENTIFIER>
AWS_SECRET_ACCESS_KEY=<AWS_USER_KEY_SECRET>

S3_BUCKET=<NAME_OF_BUCKET_TO_SEND_QUERY_RESULTS_TO>
GLUE_CATALOG_NAME=<NAME_OF_CATALOG_TO_QUERY>
```

# Python

- Create a venv
    - `python -m venv .venv`
- Install dependencies
    - `pip install -r requirements.txt`

## Scripts

<!-- List of sections for each file that is a script in this directory. -->

## Modules

<!-- List of sections for each file that is a module in this directory. -->

## Testing

- All the python utilty modules have associated test files in the format `test_<module_name>.py`
- <!-- Include the conftest line if it has been used. -->
- `conftest.py` provides test fixtures for those tests
- To run the test suite
    - `pytest *.py`
    - OR
    - `pytes *.py -vvx` for more information.

<!-- Optional sections that may be of use. -->

# Docker

## `Dockerfile`

- <!-- Purpose of Dockerfile. What it builds? Lambda etc. -->
- <!-- Command to build image. -->

<!------------------------------------------->

### `pipeline`

- <!-- Script description. -->
- <!-- Base command to run. -->
- - <!-- Any additional commands that may be useful. -->

### `extract`

- <!-- Module description. -->
- <!-- Key function signiatures. -->

### `transform`

- <!-- Module description. -->
- <!-- Key function signiatures. -->

### `load`

- <!-- Module description. -->
- <!-- Key function signiatures. -->
