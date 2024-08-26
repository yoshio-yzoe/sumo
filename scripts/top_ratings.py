import os
import csv
from collections import defaultdict
import argparse


def load_rikishi_data(csv_path='../csvs/rikishi_list.csv'):
    """力士リストCSVから力士IDと四股名（英語・日本語）の対応を読み込む"""
    rikishi_data = {}
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rikishi_data[row['ID']] = {
                'shikona_en': row['Shikona (EN)'],
                'shikona_jp': row['Shikona (JP)']
            }
    return rikishi_data


import re

def extract_top_ratings(ratings_dir, top_n, rikishi_data):
    all_ratings = defaultdict(lambda: {'max_rating': 0, 'details': {}})
    pattern = re.compile(r'^rating_(\d{4})(\d{2})\.csv$')

    for filename in os.listdir(ratings_dir):
        match = pattern.match(filename)
        if match:
            try:
                year, month = map(int, match.groups())
                with open(os.path.join(ratings_dir, filename), 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        rikishi_id = row['RikishiID']
                        for day in range(1, 16):
                            try:
                                rating = float(row[f'{day}_rating'])
                                if rating > all_ratings[rikishi_id]['max_rating']:
                                    all_ratings[rikishi_id] = {
                                        'max_rating': rating,
                                        'details': {
                                            'rating': rating,
                                            'year': year,
                                            'month': month,
                                            'day': day
                                        }
                                    }
                            except (KeyError, ValueError):
                                continue  # Skip this day if there's an error
            except Exception as e:
                print(f"Error processing file {filename}: {e}")
                continue  # Skip this file if there's an error

    # Sort by max_rating and get top N
    top_ratings = sorted(all_ratings.items(), key=lambda x: x[1]['max_rating'], reverse=True)[:top_n]

    return [
        {
            'rikishi_id': rikishi_id,
            'shikona_en': rikishi_data.get(rikishi_id, {}).get('shikona_en', 'Unknown'),
            'shikona_jp': rikishi_data.get(rikishi_id, {}).get('shikona_jp', '不明'),
            'rating': details['max_rating'],
            'year': details['details']['year'],
            'month': details['details']['month'],
            'day': details['details']['day']
        }
        for rikishi_id, details in top_ratings
    ]

def get_basho_name(month):
    """月を場所名に変換する"""
    basho_names = {
        1: "初場所", 3: "春場所", 5: "夏場所",
        7: "名古屋場所", 9: "秋場所", 11: "九州場所"
    }
    return basho_names.get(month, "場所")


def main():
    parser = argparse.ArgumentParser(description='Extract top N highest rated rikishi from historical data.')
    parser.add_argument('top_n', type=int, help='Number of top rated rikishi to extract')
    args = parser.parse_args()

    try:
        rikishi_data = load_rikishi_data()
        ratings_dir = '../csvs/rating'
        output_file = f'../csvs/rating/top_{args.top_n}_ratings.csv'

        top_ratings = extract_top_ratings(ratings_dir, args.top_n, rikishi_data)

        if not top_ratings:
            print("No ratings data found or processed. Please check your data files.")
            return

        # Write to CSV
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['rikishi_id', 'shikona_en', 'shikona_jp', 'rating', 'year', 'month',
                                                   'day'])
            writer.writeheader()
            for rating in top_ratings:
                writer.writerow(rating)

        print(f"Top {args.top_n} ratings have been written to {output_file}")

        # Display results in terminal
        print("\nTop Ratings:")
        print("============")
        for rank, rating in enumerate(top_ratings, 1):
            basho_name = get_basho_name(rating['month'])
            print(f"{rank}. {rating['shikona_en']} ({rating['shikona_jp']}):")
            print(f"   Rating: {rating['rating']:.2f}")
            print(f"   Date: {rating['year']}年{basho_name}{rating['day']:02d}日目")
            print()

    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please check your input data and try again.")


if __name__ == "__main__":
    main()