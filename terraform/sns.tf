resource "aws_sns_topic" "sports_alerts" {
  name = "sports-alerts"
}

resource "aws_sns_topic_subscription" "sms" {
  topic_arn = aws_sns_topic.sports_alerts.arn
  protocol  = "sms"
  endpoint  = var.phone_number
}