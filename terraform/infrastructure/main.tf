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

data "aws_iam_policy_document" "step-function-permissions-doc" {   
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
        actions = ["lambda:InvokeFunction"]
        resources = [
                "arn:aws:lambda:eu-west-2:129033205317:function:c17-quake-notification-lambda:$LATEST",
                "arn:aws:lambda:eu-west-2:129033205317:function:c17-quake-pipeline-lambda:$LATEST"
            ]
    }
}

data "aws_iam_policy_document" "scheduler-permissions-doc" {
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
      actions = ["stateMachine:StartExecution"]
      resources = [
              "arn:aws:states:eu-west-2:129033205317:stateMachine:c17-quake-pipeline-sf-tf"
    ]
  }
}

data "aws_iam_policy_document" "report-scheduler-permissions-doc" {
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
      actions = ["lambda:InvokeFunction"]
      resources = [
              "arn:aws:lambda:eu-west-2:129033205317:function:c17-quake-report-lambda-tf"
    ]
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

data "aws_iam_policy_document" "step-function-role-trust-policy-doc" {
    statement {
      effect = "Allow"
      principals {
        type = "Service"
        identifiers = [ "states.amazonaws.com" ]
      }
      actions = [
        "sts:AssumeRole"
      ]
  }
}

data "aws_iam_policy_document" "scheduler-role-trust-policy-doc" {
  statement {
    effect = "Allow"
    principals {
      type = "Service"
      identifiers = ["scheduler.amazonaws.com"]
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

resource "aws_iam_role" "sfn_role" {
    name = "c17-quake-pipeline-step-function-terraform-role"
    assume_role_policy = data.aws_iam_policy_document.step-function-role-trust-policy-doc.json
}

resource "aws_iam_role" "scheduler_role" {
  name = "c17-quake-step-function-scheduler-role"
  assume_role_policy = data.aws_iam_policy_document.scheduler-role-trust-policy-doc.json
}

resource "aws_iam_role" "report-scheduler-role" {
  name = "c17-quake-report-scheduler-role"
  assume_role_policy = data.aws_iam_policy_document.scheduler-role-trust-policy-doc.json
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

resource "aws_iam_policy" "step-function-role-permissions-policy" {
    name = "c17-quake-pipeline-step-function-terraform-permissions-policy"
    policy = data.aws_iam_policy_document.step-function-permissions-doc.json
}

resource "aws_iam_policy" "scheduler-role-permissions-policy" {
    name = "c17-quake-sf-scheduler-terraform-permissions-policy"
    policy = data.aws_iam_policy_document.scheduler-permissions-doc.json
}

resource "aws_iam_policy" "report-scheduler-role-permissions-policy" {
    name = "c17-quake-report-scheduler-terraform-permissions-policy"
    policy = data.aws_iam_policy_document.report-scheduler-permissions-doc.json
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

resource "aws_iam_role_policy_attachment" "pipeline-step-function-role-policy-connection" {
  role = aws_iam_role.sfn_role.name
  policy_arn = aws_iam_policy.step-function-role-permissions-policy.arn
}

resource "aws_iam_role_policy_attachment" "scheduler-role-policy-connection" {
  role = aws_iam_role.scheduler_role.name
  policy_arn = aws_iam_policy.scheduler-role-permissions-policy.arn
}

resource "aws_iam_role_policy_attachment" "report-scheduler-role-policy-connection" {
  role = aws_iam_role.report-scheduler-role.name
  policy_arn = aws_iam_policy.report-scheduler-role-permissions-policy.arn
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

# Pipeline Step Function
resource "aws_sfn_state_machine" "sfn-state-machine" {
  name     = "c17-quake-pipeline-sf-tf"
  role_arn = aws_iam_role.sfn_role.arn

  definition = <<EOF
{
  "Comment": "Pipeline and alert state machine.",
  "StartAt": "Pipeline Lambda",
  "States": {
    "Pipeline Lambda": {
      "Type": "Task",
      "Resource": "arn:aws:states:::lambda:invoke",
      "Output": "{% $states.result.Payload %}",
      "Arguments": {
        "FunctionName": "arn:aws:lambda:eu-west-2:129033205317:function:c17-quake-pipeline-lambda:$LATEST",
        "Payload": "{% $states.input %}"
      },
      "Retry": [
        {
          "ErrorEquals": [
            "Lambda.ServiceException",
            "Lambda.AWSLambdaException",
            "Lambda.SdkClientException",
            "Lambda.TooManyRequestsException"
          ],
          "IntervalSeconds": 1,
          "MaxAttempts": 3,
          "BackoffRate": 2,
          "JitterStrategy": "FULL"
        }
      ],
      "Next": "Notification Lambda"
    },
    "Notification Lambda": {
      "Type": "Task",
      "Resource": "arn:aws:states:::lambda:invoke",
      "Output": "{% $states.result.Payload %}",
      "Arguments": {
        "FunctionName": "arn:aws:lambda:eu-west-2:129033205317:function:c17-quake-notification-lambda:$LATEST",
        "Payload": "{% $states.input %}"
      },
      "Retry": [
        {
          "ErrorEquals": [
            "Lambda.ServiceException",
            "Lambda.AWSLambdaException",
            "Lambda.SdkClientException",
            "Lambda.TooManyRequestsException"
          ],
          "IntervalSeconds": 1,
          "MaxAttempts": 3,
          "BackoffRate": 2,
          "JitterStrategy": "FULL"
        }
      ],
      "End": true
    }
  },
  "QueryLanguage": "JSONata"
}
EOF
}

# Step Function Scheduler
resource "aws_scheduler_schedule" "step-function-schedule" {
  name       = "c17-quake-step-function-scheduler-tf"
  group_name = "default"

  flexible_time_window {
    mode = "OFF"
  }

  schedule_expression =  "cron(*/1 * * * ? *)"

  target {
    arn      = aws_sfn_state_machine.sfn-state-machine.arn
    role_arn = aws_iam_role.scheduler_role.arn
  }
}

# Report Scheduler
resource "aws_scheduler_schedule" "report-lambda-schedule" {
  name       = "c17-quake-report-scheduler-tf"
  group_name = "default"

  flexible_time_window {
    mode = "OFF"
  }

  schedule_expression =  "cron(0 0 * * ? *)"

  target {
    arn      = aws_lambda_function.report-lambda.arn
    role_arn = aws_iam_role.scheduler_role.arn
  }
}