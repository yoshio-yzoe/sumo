import os
import csv
import math
from collections import defaultdict


def calculate_elo(ra, rb, k, sa):
    ea = 1 / (1 + 10 ** ((rb - ra) / 400))
    return ra + k * (sa - ea)


def process_matches(file_path):
    matches = defaultdict(list)
    rikishi_info = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            matches[int(row['Day'])].append(row)
            # 東西両方の力士の情報を記録
            rikishi_info[row['EastId']] = row['EastShikona']
            rikishi_info[row['WestId']] = row['WestShikona']
    return matches, rikishi_info


def update_ratings(matches, rikishi_info, ratings, basho):
    daily_ratings = defaultdict(lambda: defaultdict(lambda: {'rating': 1500, 'shikona': ''}))

    # Initialize ratings from previous basho
    for rikishi_id, data in ratings.items():
        daily_ratings[0][rikishi_id] = {'rating': data['rating'], 'shikona': data['shikona']}

    for day in range(1, 16):
        # Copy ratings from previous day
        for rikishi_id, data in daily_ratings[day - 1].items():
            daily_ratings[day][rikishi_id] = data.copy()

        # Process matches for the day
        for match in matches.get(day, []):
            winner_id = match['WinnerId']
            loser_id = match['EastId'] if match['WestId'] == winner_id else match['WestId']

            # Ensure both rikishi are in the ratings and have shikona
            for rikishi_id in [winner_id, loser_id]:
                if rikishi_id not in daily_ratings[day] or not daily_ratings[day][rikishi_id]['shikona']:
                    daily_ratings[day][rikishi_id] = {
                        'rating': 1500,
                        'shikona': rikishi_info.get(rikishi_id, f"Unknown-{rikishi_id}")
                    }

            winner_rating = daily_ratings[day][winner_id]['rating']
            loser_rating = daily_ratings[day][loser_id]['rating']

            new_winner_rating = calculate_elo(winner_rating, loser_rating, 16, 1)
            new_loser_rating = calculate_elo(loser_rating, winner_rating, 16, 0)

            daily_ratings[day][winner_id]['rating'] = new_winner_rating
            daily_ratings[day][loser_id]['rating'] = new_loser_rating

    return daily_ratings


def save_ratings(ratings, output_dir):
    for basho, daily_ratings in ratings.items():
        output_file = os.path.join(output_dir, f'rating_{basho}.csv')
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['RikishiID', 'Shikona', 'Basho'] + [f'{i}_rating' for i in range(1, 16)])

            for rikishi_id in daily_ratings[15].keys():
                row = [rikishi_id, daily_ratings[15][rikishi_id]['shikona'], basho]
                for day in range(1, 16):
                    row.append(daily_ratings[day][rikishi_id]['rating'])
                writer.writerow(row)


def has_jonokuchi(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return any(row['Kubun'] == 'Jonokuchi' for row in reader)


def main():
    input_dir = 'csvs'
    output_dir = 'csvs/rating'
    os.makedirs(output_dir, exist_ok=True)

    ratings = defaultdict(lambda: defaultdict(lambda: {'rating': 1500, 'shikona': ''}))

    for file_name in sorted(os.listdir(input_dir)):
        if file_name.startswith('matches_') and file_name.endswith('.csv'):
            file_path = os.path.join(input_dir, file_name)

            # Check if the file contains Jonokuchi matches
            if not has_jonokuchi(file_path):
                continue

            basho = file_name[8:14]  # Extract YYYYMM from filename
            matches, rikishi_info = process_matches(file_path)
            daily_ratings = update_ratings(matches, rikishi_info, ratings[basho], basho)

            # Update ratings for the next basho
            for rikishi_id, data in daily_ratings[15].items():
                ratings[basho][rikishi_id] = data

            save_ratings({basho: daily_ratings}, output_dir)
            print(file_name, "end")

if __name__ == "__main__":
    main()