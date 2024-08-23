import requests
import pandas as pd
import numpy as np
import os

# APIのベースURL
BASE_URL = "http://www.sumo-api.com/api/rikishi/"

# イロレーティング計算のKファクターを32に変更
K_FACTOR = 32


def calculate_elo(win_rating, lose_rating, K=K_FACTOR):
    expected_win = 1 / (1 + 10 ** ((lose_rating - win_rating) / 400))
    win_rating += K * (1 - expected_win)
    lose_rating -= K * expected_win
    return win_rating, lose_rating


def get_matches(rikishi_id):
    """APIから力士の試合データを取得し、DataFrameとして返す"""
    matches_url = f"{BASE_URL}{rikishi_id}/matches"
    try:
        response = requests.get(matches_url, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data['records']:
            return pd.DataFrame(data['records'])
    except requests.RequestException as e:
        print(f"Error retrieving matches for rikishi ID {rikishi_id}: {e}")
    return pd.DataFrame()


def get_initial_rating(rank):
    """番付に基づいて初期レーティングを返す"""
    if 'Makuuchi' in rank:
        return 1800
    elif 'Juryo' in rank:
        return 1700
    return 1500  # デフォルトレーティング


def process_rikishi(rikishi_id, shikona):
    """特定の力士の試合データを処理してレーティングを計算する"""
    df = get_matches(rikishi_id)
    if df.empty:
        return pd.DataFrame()

    ratings = {}
    results = []

    for index, match in df.iterrows():
        basho_day = int(f"{match['bashoId']}{match['day']:02d}")
        winner_id = match['winnerId']
        loser_id = match['eastId'] if match['westId'] == winner_id else match['westId']

        if winner_id not in ratings:
            ratings[winner_id] = get_initial_rating(
                match['eastRank'] if match['eastId'] == winner_id else match['westRank'])
        if loser_id not in ratings:
            ratings[loser_id] = get_initial_rating(
                match['eastRank'] if match['eastId'] == loser_id else match['westRank'])

        # Calculate new ratings
        new_winner_rating, new_loser_rating = calculate_elo(ratings[winner_id], ratings[loser_id])

        # Update ratings in the dictionary
        ratings[winner_id] = new_winner_rating
        ratings[loser_id] = new_loser_rating

        # Only update the result for the rikishi of interest
        if rikishi_id == winner_id:
            current_rating = new_winner_rating
        elif rikishi_id == loser_id:
            current_rating = new_loser_rating
        else:
            continue  # Skip if neither winner nor loser is the rikishi of interest

        result = {'ID': rikishi_id, 'Shikona': shikona, 'BashoDay': basho_day, 'Rating': current_rating}
        results.append(result)

    return pd.DataFrame(results)


def main():
    rikishi_df = pd.read_csv('../csvs/rikishi_list.csv')
    all_results = []

    for _, row in rikishi_df.iterrows():
        rikishi_results = process_rikishi(row['ID'], row['Shikona (EN)'])
        all_results.append(rikishi_results)

    final_df = pd.concat(all_results, ignore_index=True)
    final_df.to_csv('../csvs/test/all_ratings.csv', index=False)
    print("All ratings have been calculated and saved.")


if __name__ == "__main__":
    main()
