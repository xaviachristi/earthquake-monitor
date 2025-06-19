provider "aws" {
    region = var.AWS_REGION
    access_key = var.AWS_ACCESS_KEY
    secret_key = var.AWS_SECRET_KEY
}

# Images
data "aws_ecr_image" "pipeline-image" {
    repository_name = "c17-quake-pipeline-ecr-tf"
    image_tag = "latest"
}

data "aws_ecr_image" "notification-image" {
    repository_name = "c17-quake-notification-ecr-tf"
    image_tag = "latest"
}

data "aws_ecr_image" "report-image" {
    repository_name = "c17-quake-report-ecr-tf"
    image_tag = "latest"
}

# Permissions Docs
data "aws_iam_policy_document" "pipeline-lambda-permissions-doc" {
     statement {
      effect = "Allow"
      actions = [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ]
      resources = [ "arn:aws:logs:eu-west-2:129033205317:*" ]
    }
    statement {
        effect = "Allow"
        actions = ["sns:ListTopics"]
        resources = ["*"]
    }
}

data "aws_iam_policy_document" "notification-lambda-permissions-doc" {
     statement {
      effect = "Allow"
      actions = [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ]
      resources = [ "arn:aws:logs:eu-west-2:129033205317:*" ]
    }
    statement {
        effect = "Allow"
        actions = [
				"sns:Publish",
				"sns:CreateTopic",
				"sns:Subscribe"
			]
        resources = ["*"]
    }
}

data "aws_iam_policy_document" "report-lambda-permissions-doc" {
     statement {
      effect = "Allow"
      actions = [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ]
      resources = [ "arn:aws:logs:eu-west-2:129033205317:*" ]
    }
    statement {
        effect = "Allow"
        actions = ["s3:*"]
        resources = ["*"]
    }
}

# Trust doc
data "aws_iam_policy_document" "lambda-role-trust-policy-doc" {
    statement {
      effect = "Allow"
      principals {
        type = "Service"
        identifiers = [ "lambda.amazonaws.com" ]
      }
      actions = [
        "sts:AssumeRole"
      ]
    }
}

# Roles
resource "aws_iam_role" "pipeline-lambda-role" {
    name = "c17-quake-pipeline-lambda-terraform-role"
    assume_role_policy = data.aws_iam_policy_document.lambda-role-trust-policy-doc.json
}

resource "aws_iam_role" "notification-lambda-role" {
    name = "c17-quake-notification-lambda-terraform-role"
    assume_role_policy = data.aws_iam_policy_document.lambda-role-trust-policy-doc.json
}

resource "aws_iam_role" "report-lambda-role" {
    name = "c17-quake-report-lambda-terraform-role"
    assume_role_policy = data.aws_iam_policy_document.lambda-role-trust-policy-doc.json
}

# Permissions policies
resource "aws_iam_policy" "pipeline-lambda-role-permissions-policy" {
    name = "c17-quake-pipeline-lambda-terraform-permissions-policy"
    policy = data.aws_iam_policy_document.pipeline-lambda-permissions-doc.json
}

resource "aws_iam_policy" "notification-lambda-role-permissions-policy" {
    name = "c17-quake-notification-lambda-terraform-permissions-policy"
    policy = data.aws_iam_policy_document.notification-lambda-permissions-doc.json
}

resource "aws_iam_policy" "report-lambda-role-permissions-policy" {
    name = "c17-quake-report-lambda-terraform-permissions-policy"
    policy = data.aws_iam_policy_document.report-lambda-permissions-doc.json
}

# Connect the policies to the role
resource "aws_iam_role_policy_attachment" "pipeline-lambda-role-policy-connection" {
  role = aws_iam_role.pipeline-lambda-role.name
  policy_arn = aws_iam_policy.pipeline-lambda-role-permissions-policy.arn
}

resource "aws_iam_role_policy_attachment" "notification-lambda-role-policy-connection" {
  role = aws_iam_role.notification-lambda-role.name
  policy_arn = aws_iam_policy.notification-lambda-role-permissions-policy.arn
}

resource "aws_iam_role_policy_attachment" "report-lambda-role-policy-connection" {
  role = aws_iam_role.report-lambda-role.name
  policy_arn = aws_iam_policy.report-lambda-role-permissions-policy.arn
}

# Lambdas
resource "aws_lambda_function" "pipeline-lambda" {
  function_name = "c17-quake-pipeline-lambda-tf"
  role = aws_iam_role.pipeline-lambda-role.arn
  package_type = "Image"
  image_uri = data.aws_ecr_image.pipeline-image.image_uri
  timeout = 60
  environment {
    variables = {
        DB_USER = var.DB_USER,
        DB_HOST = var.DB_HOST,
        DB_NAME = var.DB_NAME,
        DB_PASSWORD = var.DB_PASSWORD,
        DB_PORT = var.DB_PORT,
        GEO_API_KEY = var.GEO_API_KEY
    }
  }
}

resource "aws_lambda_function" "notification-lambda" {
  function_name = "c17-quake-notification-lambda-tf"
  role = aws_iam_role.notification-lambda-role.arn
  package_type = "Image"
  image_uri = data.aws_ecr_image.notification-image.image_uri
  timeout = 60
}

resource "aws_lambda_function" "report-lambda" {
  function_name = "c17-quake-report-lambda-tf"
  role = aws_iam_role.report-lambda-role.arn
  package_type = "Image"
  image_uri = data.aws_ecr_image.report-image.image_uri
  timeout = 60
  environment {
    variables = {
        DB_USER = var.DB_USER,
        DB_HOST = var.DB_HOST,
        DB_NAME = var.DB_NAME,
        DB_PASSWORD = var.DB_PASSWORD,
        DB_PORT = var.DB_PORT,
        S3_BUCKET = var.S3_BUCKET_NAME
    }
  }
}