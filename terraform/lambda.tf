resource "aws_lambda_function" "sports_alerts" {
  function_name    = "sports-alerts"
  filename         = "../Backend/sports_alerts.zip"
  runtime          = "python3.12"
  handler          = "sports_alerts.lambda_handler"
  role             = aws_iam_role.lambda_role.arn
  source_code_hash = filebase64sha256("../Backend/sports_alerts.zip")
  timeout          = 30

}