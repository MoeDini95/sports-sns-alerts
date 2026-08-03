resource "aws_cloudwatch_event_rule" "epl_schedule" {
  name                = "epl-game-schedule"
  description         = "Triggers Lambda function during EPL games"
  schedule_expression = "cron(*/5 12-22 * 1-5,8-12 ? *)"

}

resource "aws_cloudwatch_event_rule" "nba_schedule" {
  name                = "nba-game-schedule"
  description         = "Triggers Lambda function during NBA games"
  schedule_expression = "cron(*/5 20-4 * 10-12,1-6 ? *)"

}

resource "aws_cloudwatch_event_target" "epl_target" {
  rule      = aws_cloudwatch_event_rule.epl_schedule.name
  target_id = "epl-lambda-target"
  arn       = aws_lambda_function.sports_alerts.arn

}

resource "aws_cloudwatch_event_target" "nba_target" {
  rule      = aws_cloudwatch_event_rule.nba_schedule.name
  target_id = "nba-lambda-target"
  arn       = aws_lambda_function.sports_alerts.arn

}

resource "aws_lambda_permission" "eventbridge_invoke" {
  statement_id  = "AllowEventBridgeInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.sports_alerts.function_name
  principal     = "events.amazonaws.com"

}