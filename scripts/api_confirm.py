import requests

# 力士のID
rikishi_id = 3081

# APIのベースURL
base_url = "http://www.sumo-api.com/api/rikishi/"

# 総合成績を取得
stats_url = f"{base_url}{rikishi_id}/stats"
stats_response = requests.get(stats_url)
if stats_response.status_code == 200:
    print("Stats Data:")
    print(stats_response.json())
else:
    print("Failed to retrieve stats.")

# すべての試合を取得
matches_url = f"{base_url}{rikishi_id}/matches"
matches_response = requests.get(matches_url)
if matches_response.status_code == 200:
    print("Matches Data:")
    print(matches_response.json())
else:
    print("Failed to retrieve matches.")

# 特定の相手との試合を取得（例として相手のIDを3099とする）
opponent_id = 3099
matches_opponent_url = f"{base_url}{rikishi_id}/matches/{opponent_id}"
matches_opponent_response = requests.get(matches_opponent_url)
if matches_opponent_response.status_code == 200:
    print("Matches with Specific Opponent Data:")
    print(matches_opponent_response.json())
else:
    print("Failed to retrieve matches with specific opponent.")
