resource "aws_cloudwatch_log_group" "lambda_logs" {
  name              = "/aws/lambda/sports-alerts"
  retention_in_days = 14

}

resource "aws_cloudwatch_metric_alarm" "errors_alarm" {
  alarm_name          = "Errors"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = 1
  metric_name         = "Errors"
  namespace           = "AWS/Lambda"
  period              = 300
  statistic           = "Sum"
  threshold           = 1
  alarm_description   = "This alarm is for monitoring errors within lambda"
  dimensions = {

    FunctionName = aws_lambda_function.sports_alerts.function_name

  }

}


resource "aws_cloudwatch_metric_alarm" "lambda_throttles" {
  alarm_name          = "Throttles"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = 1
  metric_name         = "Throttles"
  namespace           = "AWS/Lambda"
  period              = 300
  statistic           = "Sum"
  threshold           = 1
  alarm_description   = "This alarm is for monitoring throttles within lambda"
  dimensions = {

    FunctionName = aws_lambda_function.sports_alerts.function_name

  }

}

resource "aws_cloudwatch_metric_alarm" "lambda_duration" {
  alarm_name          = "Duration"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = 1
  metric_name         = "Duration"
  namespace           = "AWS/Lambda"
  period              = 300
  statistic           = "Average"
  threshold           = 8000
  alarm_description   = "This alarm is for monitoring durations within lambda"
  dimensions = {

    FunctionName = aws_lambda_function.sports_alerts.function_name

  }

}


resource "aws_cloudwatch_metric_alarm" "lambda_invocations" {
  alarm_name          = "Invocations"
  comparison_operator = "LessThanThreshold"
  evaluation_periods  = 1
  metric_name         = "Invocations"
  namespace           = "AWS/Lambda"
  period              = 300
  statistic           = "Sum"
  threshold           = 1
  alarm_description   = "This alarm is for monitoring Invocations within lambda"
  dimensions = {

    FunctionName = aws_lambda_function.sports_alerts.function_name

  }

}

resource "aws_cloudwatch_metric_alarm" "sns_failures" {
  alarm_name          = "SNS-Failures"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = 1
  metric_name         = "NumberOfNotificationsFailed"
  namespace           = "AWS/SNS"
  period              = 300
  statistic           = "Sum"
  threshold           = 1
  alarm_description   = "This alarm is for monitoring SNS Failures within lambda"

}
