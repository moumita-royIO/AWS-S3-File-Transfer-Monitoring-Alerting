

resource "aws_cloudwatch_event_rule" "weekly_rule" {
  name                = "weekly_summary_rule"
  schedule_expression = "cron(0 0 ? * MON *)" # Every Monday at 12 AM UTC
}

resource "aws_cloudwatch_event_target" "weekly_target" {
  rule      = aws_cloudwatch_event_rule.weekly_rule.name
  target_id = "weekly_lambda"
  arn       = aws_lambda_function.weekly_summary.arn
}

resource "aws_lambda_permission" "allow_eventbridge" {
  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.weekly_summary.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.weekly_rule.arn
}

resource "aws_lambda_permission" "allow_s3_to_invoke" {
  statement_id  = "AllowExecutionFromS3"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.immediate_alert.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.prod.arn
}
