import os
import requests
import subprocess
from datetime import datetime, timedelta

API_BASE_URL = "http://www.sumo-api.com/api"

def run_rikishi_nayose():
    print("Running rikishi_nayose.py...")
    try:
        result = subprocess.run(["python", "rikishi_nayose.py"], check=True, capture_output=True, text=True)
        print("rikishi_nayose.py completed successfully.")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error running rikishi_nayose.py: {e}")
        print("Continuing with the update process...")

def get_latest_basho():
    current_date = datetime.now()

    # 現在の日付から過去6ヶ月分の場所を確認
    for _ in range(6):
        basho_id = current_date.strftime("%Y%m")
        response = requests.get(f"{API_BASE_URL}/basho/{basho_id}")

        if response.status_code == 200:
            basho_data = response.json()
            year = int(basho_id[:4])
            month = int(basho_id[4:])
            print(f"Latest basho found: {year}-{month:02d}")
            return datetime(year, month, 1)

        # 前の奇数月に移動
        current_date = current_date.replace(day=1) - timedelta(days=1)
        current_date = current_date.replace(day=1)
        if current_date.month % 2 == 0:
            current_date = current_date.replace(day=1) - timedelta(days=1)

    raise Exception("Failed to find a valid basho in the last 6 months")

def get_existing_bashos(csv_dir):
    existing_bashos = []
    for filename in os.listdir(csv_dir):
        if filename.startswith("matches_") and filename.endswith(".csv"):
            year = int(filename[8:12])
            month = int(filename[12:14])
            existing_bashos.append(datetime(year, month, 1))
    return sorted(existing_bashos)

def main():
    # First, run rikishi_nayose.py
    run_rikishi_nayose()

    csv_dir = "../csvs"
    os.makedirs(csv_dir, exist_ok=True)

    try:
        latest_basho = get_latest_basho()
    except Exception as e:
        print(f"Error getting latest basho: {e}")
        return

    existing_bashos = get_existing_bashos(csv_dir)

    if not existing_bashos:
        print("No existing data found. Starting from the beginning.")
        start_date = datetime(1958, 1, 1)
    else:
        start_date = max(existing_bashos) + timedelta(days=32)
        start_date = start_date.replace(day=1)

    current_date = start_date
    while current_date <= latest_basho:
        if current_date.month in [1, 3, 5, 7, 9, 11]:
            print(f"Processing basho: {current_date.year}-{current_date.month:02d}")

            # Run make_database.py
            subprocess.run(["python", "make_database.py", str(current_date.year), str(current_date.month)])

            # Run elo_rating.py
            subprocess.run(["python", "elo_rating.py", str(current_date.year), str(current_date.month)])

        # Move to next month
        current_date += timedelta(days=32)
        current_date = current_date.replace(day=1)

    print("Update completed successfully.")

if __name__ == "__main__":
    main()