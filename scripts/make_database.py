import requests
import csv
import argparse
from datetime import datetime

class SumoDataManager:
    def __init__(self):
        self.divisions = [
            'Makuuchi', 'Juryo', 'Makushita',
            'Sandanme', 'Jonidan', 'Jonokuchi',
            'Maezumo', 'Others'
        ]

    def get_matches_by_basho_and_day_and_division(self, basho, day, division):
        url = f'http://www.sumo-api.com/api/basho/{basho}/torikumi/{division}/{day}'
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                matches = data.get('torikumi')
                return matches
            else:
                print(f"Failed to fetch matches: HTTP {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None

    def save_matches_to_csv(self, matches, filename, division):
        with open(filename, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            for match in matches:
                writer.writerow([
                    match.get('id'), match.get('bashoId'), division,
                    match.get('day'), match.get('matchNo'), match.get('eastId'),
                    match.get('eastShikona'), match.get('eastRank'), match.get('westId'),
                    match.get('westShikona'), match.get('westRank'), match.get('kimarite'),
                    match.get('winnerId'), match.get('winnerEn'), match.get('winnerJp')
                ])

    def record_all_matches(self, year, month):
        basho = f'{year}{month:02d}'
        filename = f'../csvs/matches_{basho}.csv'
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['ID', 'BashoId', 'Kubun', 'Day', 'MatchNo', 'EastId', 'EastShikona', 'EastRank', 'WestId',
                             'WestShikona', 'WestRank', 'Kimarite', 'WinnerId', 'WinnerEn', 'WinnerJp'])

        for division in self.divisions:
            for day in range(1, 16):
                matches = self.get_matches_by_basho_and_day_and_division(basho, day, division)
                if matches:
                    self.save_matches_to_csv(matches, filename, division)

def main():
    parser = argparse.ArgumentParser(description='Generate and process sumo tournament (basho) data.')
    parser.add_argument('year', type=int, help='Year of the basho')
    parser.add_argument('month', type=int, choices=[1, 3, 5, 7, 9, 11], help='Month of the basho')

    args = parser.parse_args()

    manager = SumoDataManager()
    manager.record_all_matches(args.year, args.month)

if __name__ == '__main__':
    main()