# Setup

- These are Terraform deploy scripts for deploying data storage infrastructure to AWS:
    - ECR repositories
- It uses the variables defined in a `terraform.tfvars` file that are used by `variables.tf`

## Install dependencies

- Terraform with brew
    - `brew tap hashicorp/tap`
    - `brew install hashicorp/tap/terraform`
- If `brew` is not installed but still on Mac run:
    - `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
- If not on mac, go to:
    - [Terraform download page](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli)

## Deploy Resources

- `terraform init`
    - Initialise the terraform directory
- `terraform plan`
    - Show execution plan for main.tf
- `terraform apply`
    - Execute main.tf
    - Creates resources
- Run pipeline shell script
    - go to scripts directory, `cd ../../scripts`
    - run pipeline script, `source upload_to_bucket.sh`
- Update configuration file
    - Update pipeline and dashboard `.env` file to include `S3_BUCKET` with the output from terraform
- Update `terraform.tfvars` in pipeline and dashboard deploy config
    - Update `AWS_S3_BUCKET_NAME` with output from terraform

## Output

- `terraform output`
    - Query output data from execution
    - Defined outputs in `outputs.tf`

## Clean Up

- `terraform destroy`
    - Deletes all resources that are made with the `apply`