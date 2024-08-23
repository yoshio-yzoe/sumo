import os
import csv
import math
from collections import defaultdict
import argparse

class EloRatingCalculator:
    def __init__(self):
        self.ratings = defaultdict(lambda: {'rating': 1500, 'shikona': ''})

    @staticmethod
    def calculate_elo(ra, rb, k, sa):
        ea = 1 / (1 + 10 ** ((rb - ra) / 400))
        return ra + k * (sa - ea)

    def process_matches(self, file_path):
        matches = defaultdict(list)
        rikishi_info = {}
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                matches[int(row['Day'])].append(row)
                rikishi_info[row['EastId']] = row['EastShikona']
                rikishi_info[row['WestId']] = row['WestShikona']
        return matches, rikishi_info

    def update_ratings(self, matches, rikishi_info, basho):
        daily_ratings = defaultdict(lambda: defaultdict(lambda: {'rating': 0, 'shikona': ''}))

        # Initialize ratings for this basho
        for rikishi_id, data in self.ratings.items():
            daily_ratings[0][rikishi_id] = data.copy()

        for day in range(1, 16):
            # Copy ratings from previous day
            for rikishi_id, data in daily_ratings[day - 1].items():
                daily_ratings[day][rikishi_id] = data.copy()

            for match in matches.get(day, []):
                winner_id = match['WinnerId']
                loser_id = match['EastId'] if match['WestId'] == winner_id else match['WestId']

                for rikishi_id in [winner_id, loser_id]:
                    if rikishi_id not in daily_ratings[day]:
                        # New rikishi, initialize with 1500
                        daily_ratings[day][rikishi_id] = {
                            'rating': 1500,
                            'shikona': rikishi_info.get(rikishi_id, f"Unknown-{rikishi_id}")
                        }

                winner_rating = daily_ratings[day][winner_id]['rating']
                loser_rating = daily_ratings[day][loser_id]['rating']

                new_winner_rating = self.calculate_elo(winner_rating, loser_rating, 16, 1)
                new_loser_rating = self.calculate_elo(loser_rating, winner_rating, 16, 0)

                daily_ratings[day][winner_id]['rating'] = new_winner_rating
                daily_ratings[day][loser_id]['rating'] = new_loser_rating

        # Update the overall ratings after the basho
        for rikishi_id, data in daily_ratings[15].items():
            self.ratings[rikishi_id] = data

        return daily_ratings

    @staticmethod
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

    def process_basho(self, year, month):
        input_dir = '../csvs'
        output_dir = '../csvs/rating'
        os.makedirs(output_dir, exist_ok=True)

        basho = f'{year}{month:02d}'
        file_name = f'matches_{basho}.csv'
        file_path = os.path.join(input_dir, file_name)

        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return

        matches, rikishi_info = self.process_matches(file_path)
        daily_ratings = self.update_ratings(matches, rikishi_info, basho)

        self.save_ratings({basho: daily_ratings}, output_dir)
        print(f"Processed {file_name}")


def has_jonokuchi(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return any(row['Kubun'] == 'Jonokuchi' for row in reader)
def main():
    parser = argparse.ArgumentParser(description='Calculate Elo ratings for sumo wrestlers.')
    parser.add_argument('--year', type=int, help='Year of the basho (optional)')
    parser.add_argument('--month', type=int, choices=[1, 3, 5, 7, 9, 11], help='Month of the basho (optional)')

    args = parser.parse_args()

    calculator = EloRatingCalculator()
    input_dir = '../csvs'

    if args.year and args.month:
        # Process specific basho
        basho = f'{args.year}{args.month:02d}'
        file_path = os.path.join(input_dir, f'matches_{basho}.csv')
        if os.path.exists(file_path) and has_jonokuchi(file_path):
            calculator.process_basho(args.year, args.month)
        else:
            print(f"Skipping {basho} as it doesn't exist or doesn't contain Jonokuchi matches")
    else:
        # Process all available data
        for file_name in sorted(os.listdir(input_dir)):
            if file_name.startswith('matches_') and file_name.endswith('.csv'):
                file_path = os.path.join(input_dir, file_name)
                if has_jonokuchi(file_path):
                    year = int(file_name[8:12])
                    month = int(file_name[12:14])
                    calculator.process_basho(year, month)
                    print(f"Processed {file_name}")
                else:
                    print(f"Skipping {file_name} as it doesn't contain Jonokuchi matches")

if __name__ == "__main__":
    main()