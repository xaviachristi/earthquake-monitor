# Notifications

This directory contains all the necessary files to run and deploy the notification script and lambda for this project. This script takes in a list of dictionaries and sends appropriately formatted email notifications via AWS SNS to emails that are subscribed to each topic (the topic is passed in as part of the script). It also contains a script that creates a `.txt` file in the format of a notification for testing purposes.

## Configuration

- The notification script is made to be used by a lambda function, and it can access certain variables through AWS when its uploaded there.
- If wanting to be ran locally, it will require the addition of loading local variables defined in a `.env` file.
- The file should contain the following variables:
```sh
AWS_ACCESS_KEY_ID=<personal-aws-key>
AWS_SECRET_ACCESS_KEY=<personal-aws-secret-key>
```

## Docker

- The Dockerfile defines the image for this lambda function.
- This allows the lambda to be ran as a container.
- To build the image.
- `docker build --provenance=false --platform=linux/amd64  -t <image-name>:latest .`
- To run the container locally.
- `docker run --platform=linux/amd64 --env-file .env`

## Running the pipeline in the cloud

- The script can be run in AWS cloud.
- To do this it is built as a lambda image and uploaded to an elastic container registry in AWS.
- Run the `docker_build` script detailed below with your details to upload the pipeline.
- After ECR deployment you will need to create a lambda function that uses your image.
- That lambda function can now be triggered and targeted by other AWS services.
- Services will need to provide the lambda with a payload to define the details for the alert that will be processed.
- The payload should take this form:
```json
{
  "message": [{"topic_arn": <arn for the topic>,
                "magnitude": <float of the magnitude of the earthquake>,
                "state_name": <name of the state the earthquake occurred in>,
                "region_name": <name of the region the earthquake occurred in>,
                "time": <time the earthquake occurred at as a string in a YYYY-MM-DD HH:MM format>,
                "tsunami": <boolean value about whether a tsunami is expected to occur or not>,
                "latitude": <float of a valid latitude coordinate>,
                "longitude": <float of a valid longitude coordinate>}]
}
```
- Example payload for a one minute window that runs one minute behind current time:
```json
{
  "message": [{"topic_arn": "arn:aws:sns:eu-west-2:129033205317:c17-quake-57-p124141-m471447-770",
                "magnitude": 3.1,
                "state_name": "Not in the USA",
                "region_name": "Taiwan",
                "time": "2025-12-13 13:40",
                "tsunami": true,
                "latitude": 30.101,
                "longitude": 50.123}]
}
```

## Other Scripts

### `docker_build`

- This script connects to AWS, builds the defined image and pushes it to an ECR.
- The script has been left as an example and utilises credentials that are personal.
- The script is actually derived from the AWS ECR push commands.
- You can find your version of these commands by creating and ECR and selecting push commands in the console.
- If you want to use the example script you will need to replace as follows:
```sh
aws ecr get-login-password --region eu-west-2 | docker login --username AWS --password-stdin <aws-account-uri>
docker build --provenance=false --platform=linux/amd64  -t <ecr-name>:latest .
docker tag <ecr-name>:latest <aws-account-uri>/<ecr-name>:latest
docker push <aws-account-uri>/<ecr-name>:latest
```

## Modules

The notification lambda utilises the `notification_maker.py` module for its function. Its exact function is detailed in this section.

### `notification_maker.py`

- Creates and formats notification messages from a list of dictionaries.
- Validates data existing and being of the correct data type.
- Publishes notification messages to their respective topics.