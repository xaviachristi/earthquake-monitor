# Terraform

- This directory provides infrastructure as code for the full pipeline cloud system
- The two sub directories constitute a setup of resources that require manual input and the rest of the infrastructure

## `setup`
- Creates four elastic container registries
- They are responsible for storing the report, dashboard and pipeline images on AWS

## `infrastructure`
- Creates the full cloud architecture
- Includes lambda functions, S3 buckets, ECS services and Glue
- Responsible for serving the dashboard, sending the message notifications and updating the data

## `push_ecr` script
- This should be ran after the setup stage
- It should be ran 4 times once for each ECR repository
- It will load a docker image into an ecr
- Use the output from the setup stage
    - In format: `<ecr-address>/<image-name>`
    - Example: `129033205317.dkr.ecr.eu-west-2.amazonaws.com/c17-quake-pipeline-ecr-tf`
- The script will ask for these two inputs for completion
- The script will also ask for folder location of dockerfile
    - Give it the directory path in reference to the root repository
    - E.g. for long-term pipeline the path is `pipelines/long-term`