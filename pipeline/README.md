# Pipeline

This directory contains all the neccessary files to run and deploy the extract, transform, load pipeline fro this project. This pipeline targets a United States Geological Survey Application Programming Interface that feeds live earthquake data as they recieve it. It transforms this data into a suitable pandas DataFrame and loads it into a deployed postgres database instance. The pipeline can be run locally or be deployed to AWS Lambda using the docker configuration.

## Configuration

- This pipeline depends upon configuration defined in z `.env` file
- The file should contain the following variables:
```sh
DB_HOST=<host-address>
DB_PORT=<accessible-port>
DB_NAME=<name>
DB_PASSWORD=<password>
DB_USER=<username>

AWS_DEFAULT_REGION=<region-resources-are-in>
AWS_ACCESS_KEY_ID=<personal-aws-key>
AWS_SECRET_ACCESS_KEY=<personal-aws-secret-key>
```

## Running the pipeline locally

- The `pipeline` is ran with python and the `pipeline` script
- The `pipeline` script takes two arguments start and end
- These arguments define the time window that the `pipeline` will query the api over
- Both take hour differences as integers
- End is not required and if it is not given the current time is used
- `python3 pipeline --start 2 --end 1`
- This example command would run the pipeline and upload data from the api that occured between one and two hors ago

## Docker

- The Dockerfile defines the image for this pipeline
- This allows the pipeline to b eran as a container
- To build the image
- `docker build --provenance=false --platform=linux/amd64  -t <image-name>:latest .`
- To run the container locally
- `docker run --platform=linux/amd64 --env-file .env`

## Running the pipeline in the cloud

- The pipeline can be run in AWS cloud as well as locally
- To do this it is built as a lambda image and uploaded to an elastic container registry in AWS
- Run the `docker_build` script detailed below with your details to upload the pipeline
- After ECR deployment you will need to create a lambda function that uses your image
- That lambda function can now be triggered and targetted by other AWS services
- Services will need to provide the lambda with a payload to define the time window, that payload has to contain a start paramter and can optionally be given an end parameter
- The payload should take this form:
```json
{
    "start": <time-diff-to-add-to-start-of-window>,
    "end": <time-diff-to-add-to-end-of-window>
}
```
- Example payload for a one hour window that runs one hour behind current time:
```json
{
    "start": 2,
    "end": 1
}
```

## Other Scripts

### `docker_build`

- This script connects to AWS, builds the defined image and pushes it to an ECR
- The script has been left as an example and utilises credentials that are personal
- The script is actually derived from the AWS ECR push commands
- You can find your version of these commands by creating and ECR and selecting push commmands in the console
- If you want to use the example script you will need to replace as follows:
```sh
aws ecr get-login-password --region eu-west-2 | docker login --username AWS --password-stdin <aws-account-uri>
docker build --provenance=false --platform=linux/amd64  -t <ecr-name>:latest .
docker tag <ecr-name>:latest <aws-account-uri>/<ecr-name>:latest
docker push <aws-account-uri>/<ecr-name>:latest
```

## Modules

The pipeline utilises several modules to perform key functions such as the steps of extract, transform and load. There exact function are detailed in this section. 

### `Extract`

- Reads from https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson .

- This updates every minute but stores an hours worth of data.

    - How to avoid repeated data?

### `Transform`

- This module transforms the data recieved from the api as a catalog into a pandas DataFrame
- It also cleans and normalizes the data into datatypes that match the expectations of the deployed database
- The key function that performs every action in this module is `transform`

### `Load`

- This module loads the DataFrame into the deployed database
- It will update the earthquake tables with the new earthquake events
- It will also update the region, state and region_state_interaction table as neccessary for events that contain values for these fields that have not been populated before
- It will also check for any duplicates in the earthquake table and prevent upload of duplicate events
- This behaviour is useful when running the pipeline over the same time window or overlapping time windows
- The key function that performs every action in this module is `load`

### `Topic`

- This module creates dictionaries of topic arn keys with a list of values of the information for an earthquake that matches that topic
- This is to integrate with the solution subscription feature
- Some topic in this AWS account will be made by this subscription function and they are patterned to define a map region and magnitude of earthquake they are interested in
- This module reads those topic names and check if any of the earthquakes defined in the passed DataFrame meet those requirements
- The output takes the following form:
```python
{
    <topic-arn-1>:[<earthquake-values>],
    <topic-arn-2>:[<earthquake-values>]
}
```
- The key function that performs every action in this module is `create_topic_dictionaries`


### Thought Process (to be removed/tidied when pipeline is complete)

- Tried to use ObsPy and ObsPlus to get data from the API and convert it to a dataframe.

- ObsPlus wanted a version on python with `tkinter`. I could do this now but it seems like it could cause more issues down the line.

- I can still use ObsPy to get the data (I've considered the alternative of removing this library and calling the API directly, however it seems using obspy will make it easier to expand the project to different data sources in the future). [Helpful docs for this stage.](https://docs.obspy.org/tutorial/code_snippets/retrieving_data_from_datacenters.html#the-fdsn-web-services)

- Now the big question is how to get the `ObsPy.Catalog` object into a `pd.DataFrame`.

    - Option one: convert to JSON then use a Panda's built-in.

    - Option two: convert directly to a DataFrame.

- If I'm not getting the data in as a JSON, it makes more sense to go straight to a df. However there is write support for JSON in ObsPy.

    - What is in an ObsPy JSON? Is it just going to be the QuakeML or will it be formatted properly?

- I'm going to try the following route:  
    - `obspy.clients.fdsn.client.Client.get_events()` --`obspy.Catalog`-->
    - `obspy.io.json()` --`JSON`-->
    - `pd.read_json()` --`pd.DataFrame`--> `transform.py`.

- Converting the ObsPy catalog to JSON is fine, but getting that JSON into a dataframe is difficult, as the data has a complex structure.
