resource "aws_dynamodb_table" "sports_alerts_table" {
  name = "sports_alerts_table"
  billing_mode = "PAY_PER_REQUEST"
  
  hash_key = "team_id"
  
  attribute {
    name = "team_id"
    type = "S"
  }
}