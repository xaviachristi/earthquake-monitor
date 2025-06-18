provider "aws" {
    region = var.AWS_REGION
    access_key = var.AWS_ACCESS_KEY
    secret_key = var.AWS_SECRET_KEY
}

data "aws_ecr_image" "pipeline_image" {
    repository_name = "c17-quake-pipeline-ecr-tf"
    image_tag = "latest"
}

data "aws_ecr_image" "notification_image" {
    repository_name = "c17-quake-notification-ecr-tf"
    image_tag = "latest"
}

data "aws_ecr_image" "report_image" {
    repository_name = "c17-quake-report-ecr-tf"
    image_tag = "latest"
}

data "aws_iam_policy" "cloudwatch_full_access" {
    arn = "arn:aws:iam::aws:policy/CloudWatchLogsFullAccess"
}

data "aws_iam_policy_document" "sns_list_topics" {
    statement {
        effect = "Allow"
        actions = "sns:ListTopics"
        }
}

data "aws_iam_policy_document" "sns_notifications" {
    statement {
        effect = "Allow"
        actions = [
				"sns:Publish",
				"sns:CreateTopic",
				"sns:Subscribe"
			]
        }
}


data "aws_iam_policy_document" "lambda-role-permissions-policy-doc" {
    statement {
      effect = "Allow"
      actions = [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ]
      resources = [ "arn:aws:logs:eu-west-2:129033205317:*" ]
    }
}