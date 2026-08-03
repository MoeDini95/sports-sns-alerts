variable "aws_region" {
  description = "AWS region"
  default     = "us-east-1"

}

variable "phone_number" {
  description = "SMS number"

}

variable "lambda_function_name" {
  description = "Lambda function"
  default     = "sports-alerts"

}

variable "dynamo_table_name" {
  description = "Dynamo Table"
  default     = "sports_alerts_table"

}