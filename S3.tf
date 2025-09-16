
# S3 bucket and notifications

resource "aws_s3_bucket" "prod" {
  bucket        = var.bucket_name
  force_destroy = true

  lifecycle {
    prevent_destroy = true
  }
}

resource "aws_s3_bucket_notification" "s3_event" {
  bucket = aws_s3_bucket.prod.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.immediate_alert.arn
    events              = ["s3:ObjectCreated:*"]
  }

  depends_on = [aws_lambda_permission.allow_s3_to_invoke]
}
