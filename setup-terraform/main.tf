provider "aws" {
    region = var.AWS_REGION
    access_key = var.AWS_ACCESS_KEY
    secret_key = var.AWS_SECRET_KEY
}

resource "aws_ecr_repository" "pipeline_ecr" {
    name = "c17-quake-pipeline-ecr-tf"
    image_tag_mutability = "MUTABLE"
    image_scanning_configuration {
      scan_on_push = true
    }
    force_delete = true
}

resource "aws_ecr_repository" "notification_ecr" {
    name = "c17-quake-notification-ecr-tf"
    image_tag_mutability = "MUTABLE"
    image_scanning_configuration {
      scan_on_push = true
    }
    force_delete = true
}

resource "aws_ecr_repository" "report_ecr" {
    name = "c17-quake-report-ecr-tf"
    image_tag_mutability = "MUTABLE"
    image_scanning_configuration {
      scan_on_push = true
    }
    force_delete = true
}