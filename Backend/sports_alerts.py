import requests
import boto3
import json

AI_SUMMARIES_ENABLED = True



def get_manchester_city_game():
    url = "https://site.api.espn.com/apis/site/v2/sports/soccer/eng.1/scoreboard"
    response = requests.get(url)
    data = response.json()

    for event in data["events"]:
        competitions_list = event["competitions"]
        first_competition = competitions_list[0]
        competitors = first_competition["competitors"]
        one_team = competitors[0]
        team_info_1 = one_team["team"]
        team_name_1 = team_info_1["displayName"]

        second_team = competitors[1]
        team_info_2 = second_team["team"]
        team_name_2 = team_info_2["displayName"]

        if team_name_1 == "Manchester City" or team_name_2 == "Manchester City":
            game_id = event["id"]
            status = event["status"]["type"]["description"]

            if status in ["Scheduled", "Postponed", "Canceled"]:
                print(f"Man City game found but status is {status} - skipping")
                return None

            
            print(f"Found match: {team_name_1} vs {team_name_2} | ID: {game_id} | Status: {status}")
            return game_id  
        
    print("No Man City game today")
    return None
          

        
def get_match_details(game_id):
    url = f"https://site.api.espn.com/apis/site/v2/sports/soccer/eng.1/summary?event={game_id}"
    response = requests.get(url)
    data = response.json()
    #print(data.keys())
    print(f"found match: {game_id}")


    header = data["header"]
    competitions_list = header["competitions"]
    first_competition = competitions_list[0]
    competitors = first_competition["competitors"]


    one_team = competitors[0]
    team_name_1 = one_team["team"]["displayName"]
    score_1 = one_team["score"]

    second_team = competitors[1]
    team_name_2 = second_team["team"]["displayName"]
    score_2 = second_team["score"]


    message = f"{team_name_1} {score_1} - {team_name_2} {score_2}\n"
    
    for goal_event in data["keyEvents"]:
        if goal_event["scoringPlay"] == True:
            short_text = goal_event["shortText"]
            clock = goal_event["clock"] ["displayValue"]
            team = goal_event["team"]["displayName"]
            message += f"{clock} - {short_text} ({team})\n"

    return message 
        
         
#################### Raptors Data ####################

def get_toronto_raptors_game():
    url = "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard" 
    response = requests.get(url)
    data = response.json()

    for event in data["events"]:
        competitions_list = event["competitions"]
        first_competition = competitions_list[0]
        competitors = first_competition["competitors"]
        one_team = competitors[0]
        team_info_1 = one_team["team"]
        team_name_1 = team_info_1["displayName"]

        second_team = competitors[1]
        team_info_2 = second_team["team"]
        team_name_2 = team_info_2["displayName"]

        if team_name_1 == "Toronto Raptors" or team_name_2 == "Toronto Raptors":
            game_id = event["id"]
            status = event["status"]["type"]["description"]

            if status in ["Scheduled", "Postponed", "Canceled"]:
                print(f"Raptors game found but status is {status} - skipping")
                return None
            
            print(f"Found match: {team_name_1} vs {team_name_2} | ID: {game_id} | Status: {status}")
            return game_id
        
    print("No Raps game today")
    return None


def get_nba_match_details(game_id):
    url = f"https://site.api.espn.com/apis/site/v2/sports/basketball/nba/summary?event={game_id}"
    response = requests.get(url)
    data = response.json()
    #print(data.keys())
    print(f"found raptors match: {game_id}")


    header = data["header"]
    nba_comp_list = header["competitions"]
    first_competition = nba_comp_list[0]
    competitors = first_competition["competitors"]

    first_team = competitors[0]
    nba_team_1 = first_team["team"]["displayName"]
    final_score = first_team["score"]


    second_team = competitors[1]
    nba_team_2 = second_team["team"]["displayName"]
    final_score_2 = second_team["score"]

   


    leaders = data["leaders"] #top level data 
    team_leaders = leaders[0] #first team
    combined_stats = team_leaders["leaders"]
    points_stats = combined_stats[0]
    top_scorers = points_stats["leaders"]
    top_scorer = top_scorers[0]
    player_name = top_scorer["athlete"]["displayName"]
    player_stats = top_scorer["displayValue"]


    assists_stats = combined_stats[1]
    top_assists = assists_stats["leaders"]

    rebounds_stats = combined_stats[2]
    top_rebounds = rebounds_stats["leaders"]
    
    top_assister = top_assists[0]
    assist_player = top_assister["athlete"]["displayName"]
    assist_stats = top_assister ["displayValue"]

    top_rebounder = top_rebounds[0]
    rebound_player = top_rebounder["athlete"]["displayName"]
    rebound_stats = top_rebounder["displayValue"]

    
    message = f"{nba_team_1} {final_score} - {nba_team_2} {final_score_2}\n"
    
    message +=  (f"Top Stats:{player_name} - {player_stats} pts | {assist_player} - {assist_stats} ast | {rebound_player} - {rebound_stats} reb")
    return message


def check_and_update_state(team_id, current_score, match_id):
    # Connection to DynamoDB
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    # Selecting table 
    table = dynamodb.Table('sports_alerts_table')
    response = table.get_item(Key={"team_id": team_id})

    item = response.get("Item", {})
    last_score =  item.get("last_score", None)
    

    if last_score == current_score:
        return False
    table.put_item(
       Item={
           "team_id": team_id,
           "last_score": current_score,
           "match_id": match_id
       }
   )

    return True

def get_ai_summary(match_data):
    bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")
    model_id = "anthropic.claude-haiku-4-5-20251001-v1:0"

    body = {
         "max_tokens": 200,
         "messages": [
            {
                 "role": "user",
                 "content": f"Here is the match data:\n{match_data}\n\nWrite a short 2-3 sentence SMS summary of this match."
            }
        ],
        "anthropic_version": "bedrock-2023-05-31"
    }

    response = bedrock.invoke_model(
        body=json.dumps(body),
        modelId=model_id,
    )
    response_body = json.loads(response["body"].read())
    summary = response_body["content"][0]["text"]
    return summary


    

def lambda_handler(event, context):
    sns = boto3.client("sns", region_name="us-east-1")
    SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:259004904941:sports-alerts"
    
   


    # Man City 
    found_mancity_id = get_manchester_city_game()
    if found_mancity_id is None:
        print ("No Match information today. Man City is not playing")
    else:
        message = get_match_details(found_mancity_id)
        if check_and_update_state("manchester-city", message, found_mancity_id):
            if AI_SUMMARIES_ENABLED: 
                message = get_ai_summary(message)
            sns.publish(TopicArn=SNS_TOPIC_ARN, Message=message)
       
    
    
    
    # Raptors 
    found_raptors_id = get_toronto_raptors_game()
    #print(f"Raptors game ID: {found_raptors_id}")
    if found_raptors_id is None:
         print ("No Match information today. Raptors are not playing")
    else:
        message = get_nba_match_details(found_raptors_id)
        if check_and_update_state("toronto-raptors", message, found_raptors_id):
            if AI_SUMMARIES_ENABLED: 
                message = get_ai_summary(message)
            sns.publish(TopicArn=SNS_TOPIC_ARN, Message=message)

    return {"statusCode": 200, "body": "Done"}

if __name__ == "__main__":
    lambda_handler(None, None)
