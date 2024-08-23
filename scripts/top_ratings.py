import os
import csv
from collections import defaultdict
import argparse


def extract_top_ratings(ratings_dir, top_n):
    all_ratings = defaultdict(lambda: {'max_rating': 0, 'details': {}})

    for filename in os.listdir(ratings_dir):
        if filename.endswith('.csv'):
            year, month = int(filename[7:11]), int(filename[11:13])
            with open(os.path.join(ratings_dir, filename), 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    rikishi_id = row['RikishiID']
                    shikona = row['Shikona']
                    for day in range(1, 16):
                        rating = float(row[f'{day}_rating'])
                        if rating > all_ratings[rikishi_id]['max_rating']:
                            all_ratings[rikishi_id] = {
                                'max_rating': rating,
                                'details': {
                                    'shikona': shikona,
                                    'rating': rating,
                                    'year': year,
                                    'month': month,
                                    'day': day
                                }
                            }

    # Sort by max_rating and get top N
    top_ratings = sorted(all_ratings.items(), key=lambda x: x[1]['max_rating'], reverse=True)[:top_n]

    return [
        {
            'rikishi_id': rikishi_id,
            'shikona': details['details']['shikona'],
            'rating': details['max_rating'],
            'year': details['details']['year'],
            'month': details['details']['month'],
            'day': details['details']['day']
        }
        for rikishi_id, details in top_ratings
    ]


def main():
    parser = argparse.ArgumentParser(description='Extract top N highest rated rikishi from historical data.')
    parser.add_argument('top_n', type=int, help='Number of top rated rikishi to extract')
    parser.add_argument('--output', default='top_ratings.csv', help='Output CSV file name')
    args = parser.parse_args()

    ratings_dir = '../csvs/rating'
    top_ratings = extract_top_ratings(ratings_dir, args.top_n)

    # Write to CSV
    with open(args.output, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['rikishi_id', 'shikona', 'rating', 'year', 'month', 'day'])
        writer.writeheader()
        for rating in top_ratings:
            writer.writerow(rating)

    print(f"Top {args.top_n} ratings have been written to {args.output}")


if __name__ == "__main__":
    main()