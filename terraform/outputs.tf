output "lambda_arn" {

  description = "Lambda function ARN"
  value       = aws_lambda_function.sports_alerts.arn

}

output "sns_arn" {
  description = "SNS topic ARN"
  value       = aws_sns_topic.sports_alerts.arn

}

output "dynamodb_arn" {
  description = "DynamoDB ARN"
  value       = aws_dynamodb_table.sports_alerts_table.arn
}