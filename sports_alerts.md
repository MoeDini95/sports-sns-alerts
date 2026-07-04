# Sports Alerts AWS Project — Conversation Summary for Claude Code

## Project Overview

Build a personal sports alert system that sends SMS notifications for live scores,
box scores, and player stats for **Manchester City (EPL)** and **Toronto Raptors (NBA)**.
No data stored on phone — all backend via AWS.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.11+ |
| Compute | AWS Lambda |
| Scheduler | AWS EventBridge (cron) |
| Database | AWS DynamoDB |
| Alerts | AWS SNS (SMS to phone) |
| Monitoring | AWS CloudWatch |
| IaC | Terraform |
| CI/CD | GitHub Actions |
| AI Summaries | Claude API or Amazon Bedrock (Phase 7) |
| Secrets | AWS Secrets Manager (Phase 7) |

---

## Sports Data Source

**ESPN Unofficial Public API — Free, no API key required**

### EPL (Manchester City)
```
https://site.api.espn.com/apis/site/v2/sports/soccer/eng.1/scoreboard
https://site.api.espn.com/apis/site/v2/sports/soccer/eng.1/summary?event={gameId}
```

### NBA (Toronto Raptors)
```
https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard
https://site.api.espn.com/apis/site/v2/sports/basketball/nba/summary?event={gameId}
```

### Supported League Slugs
- `eng.1` — English Premier League
- `esp.1` — La Liga
- `ger.1` — Bundesliga
- `ita.1` — Serie A
- `fra.1` — Ligue 1
- `uefa.champions_league` — Champions League

---

## Architecture Flow

```
EventBridge (cron every 5 min)
        ↓
Lambda (Python)
        ↓
ESPN API ←→ DynamoDB (last known state)
        ↓ if state changed
SNS Topic
        ↓
SMS → Phone
```

---

## Teams Configuration

```python
TEAMS = {
    "soccer/eng.1": "manchester-city",
    "basketball/nba": "toronto-raptors"
}
```

---

## DynamoDB Schema

**Table name:** `sports_alerts_state`
**Partition key:** `team_id` (String)

### Example records:

```json
{
  "team_id": "manchester-city",
  "last_score": "2-1",
  "last_event": "halftime",
  "match_id": "abc123",
  "updated_at": "2026-06-13T14:45:00Z"
}
```

```json
{
  "team_id": "toronto-raptors",
  "last_score": "58-52",
  "last_event": "end_of_q2",
  "match_id": "xyz789",
  "updated_at": "2026-06-13T21:30:00Z"
}
```

### boto3 operations used:
```python
dynamodb.get_item()   # fetch last known state
dynamodb.put_item()   # save new state after change
```

---

## Alert Types

| Alert | Trigger |
|---|---|
| Score change | Any goal (EPL) or quarter score change (NBA) |
| Halftime summary | Status transitions to halftime |
| Final summary | Match/game ends |
| Daily digest | Scheduled once per day |

### Alert logic note:
- EPL: every goal is significant — alert on each
- NBA: consider filtering for meaningful changes only (big runs, comebacks, buzzer beaters) to reduce noise over 48 minutes

---

## CloudWatch Alarms

| Metric | Threshold | Action |
|---|---|---|
| Errors | >= 1 in 5 min | SNS → ops email |
| Throttles | >= 1 in 5 min | SNS → ops email |
| Duration | > 8000ms | SNS → ops email |
| Invocations | == 0 over 30 min during game window | SNS → ops email |
| SNS NotificationsFailed | >= 1 | SNS → ops email |

### CloudWatch Dashboard panels:
- Invocation count over time
- Error count over time
- Duration over time
- SNS messages sent count

---

## CI/CD Pipeline (GitHub Actions)

```
Push to branch  →  pytest
Merge to main   →  terraform plan → terraform apply → Lambda deploy
```

Lambda code is zipped and deployed via Terraform's `aws_lambda_function` resource.

---

## Cost Estimate

| Service | Est. Monthly Cost |
|---|---|
| ESPN API | $0 (unofficial, free) |
| Lambda | $0 (within free tier) |
| DynamoDB | $0 (within free tier) |
| EventBridge | $0 (within free tier) |
| SNS SMS (Canada) | ~$0.19–$0.77 |
| CloudWatch | $0 (within free tier) |
| Claude API (Phase 7) | ~$0.01–$0.05 (minimal at personal scale) |
| **Total (Phases 1-6)** | **~$0–$1/month** |
| **Total (with Phase 7)** | **~$0–$2/month** |

---

## Build Phases

### Phase 1 — Local Python ✅ COMPLETE
- ESPN API returning data locally for both teams
- EPL: team names, score, game ID, status, start date, goal scorers (minute + description)
- NBA: team names, final score, top scorer (points), assists leader, rebounds leader — both teams
- Graceful fallbacks for no-game days for both teams
- File: `sports_alerts.py`

### Phase 2 — Core AWS (current phase)
- Lambda + SNS + DynamoDB working (deployed manually via console first)
- Test end-to-end alert flow

### Phase 3 — Terraform
- Provision all resources as IaC
- Lambda, SNS, DynamoDB, EventBridge, IAM roles, CloudWatch log groups
- S3 + DynamoDB Terraform backend

### Phase 4 — EventBridge + Alert Logic
- Cron scheduling during game windows
- Sport-specific alert logic (EPL vs NBA differences)

### Phase 5 — CloudWatch
- Alarms and dashboard

### Phase 6 — GitHub Actions CI/CD
- Automated test → plan → apply pipeline

### Phase 7 — AI-Generated Summaries (NEW)
- Call Claude API (or Amazon Bedrock) from inside Lambda
- Pass structured match data (scores, scorers, stats) as input
- Receive natural language summary for SMS alert
- Example output: "Barrett led Toronto with a strong all-around game, dropping 21 and dishing 7 assists as the Raptors pulled away in the second half."
- New Terraform resources: AWS Secrets Manager for API key
- Updated CI/CD tests to cover AI summary generation
- Build after all other phases are stable and deployed

---

## Phase 1 Starter Code

```python
import requests

def get_manchester_city_game():
    url = "https://site.api.espn.com/apis/site/v2/sports/soccer/eng.1/scoreboard"
    response = requests.get(url)
    data = response.json()

    for event in data.get("events", []):
        competitors = event["competitions"][0]["competitors"]
        team_names = [c["team"]["displayName"] for c in competitors]

        if "Manchester City" in team_names:
            game_id = event["id"]
            status = event["status"]["type"]["description"]
            print(f"Found match: {team_names}")
            print(f"Game ID: {game_id}")
            print(f"Status: {status}")
            return game_id

    print("No Man City match today")
    return None

get_manchester_city_game()
```

**Next steps after Phase 1 starter works:**
1. Parse full box score JSON for score, status, and scorers
2. Add Raptors equivalent using NBA scoreboard endpoint
3. Add DynamoDB state comparison logic locally using boto3
4. Wrap into Lambda handler function

---

## Developer Context

- Experienced with AWS console and Terraform
- Has used boto3 in a previous project
- Less experience with Python and DynamoDB
- Located in Toronto, Canada (Ontario)
- Goal: personal use only, minimal cost, no data on phone
