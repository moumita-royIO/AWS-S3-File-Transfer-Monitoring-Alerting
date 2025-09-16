# Immediate & Weekly Lambda functions

resource "aws_lambda_function" "immediate_alert" {
  filename         = "lambda/immediate_alert.zip"
  function_name    = "s3_immediate_alert"
  handler          = "immediate_alert.lambda_handler"
  runtime          = "python3.11"
  role             = aws_iam_role.lambda_role.arn
  source_code_hash = filebase64sha256("lambda/immediate_alert.zip")

  environment {
    variables = {
      OWNER_EMAIL = var.owner_email
      BUCKET_NAME = var.bucket_name
    }
  }

  lifecycle {
    prevent_destroy = true
  }
}

resource "aws_lambda_function" "weekly_summary" {
  filename         = "lambda/weekly_summary.zip"
  function_name    = "s3_weekly_summary"
  handler          = "weekly_summary.lambda_handler"
  runtime          = "python3.11"
  role             = aws_iam_role.lambda_role.arn
  source_code_hash = filebase64sha256("lambda/weekly_summary.zip")

  environment {
    variables = {
      OWNER_EMAIL = var.owner_email
      BUCKET_NAME = var.bucket_name
    }
  }

  lifecycle {
    prevent_destroy = true
  }
}
