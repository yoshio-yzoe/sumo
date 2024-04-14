import pandas as pd
import os
import glob


def calculate_elo(win_rating, lose_rating, K=16):
    expected_win = 1 / (1 + 10 ** ((lose_rating - win_rating) / 400))
    updated_win_rating = win_rating + K * (1 - expected_win)
    updated_lose_rating = lose_rating - K * expected_win
    return updated_win_rating, updated_lose_rating


def process_basho_files(basho_files, rikishi_info, initial_rating=1500):
    # Dictionary to store ratings across all basho
    ratings_dict = {}
    rikishi_current_ratings = {}

    for file in sorted(basho_files):
        df = pd.read_csv(file)
        if df.empty:
            continue  # Ignore empty files

        basho = file.split('_')[-1].split('.')[0]

        for day in range(1, 16):  # Process each day
            day_df = df[df['Day'] == day]
            for _, row in day_df.iterrows():
                winner_id = row['WinnerId']
                loser_id = row['EastId'] if row['EastId'] != winner_id else row['WestId']

                # Set initial ratings for new rikishi or carry forward the last rating
                if winner_id not in rikishi_current_ratings:
                    rikishi_current_ratings[winner_id] = initial_rating
                if loser_id not in rikishi_current_ratings:
                    rikishi_current_ratings[loser_id] = initial_rating

                winner_rating = rikishi_current_ratings[winner_id]
                loser_rating = rikishi_current_ratings[loser_id]

                new_winner_rating, new_loser_rating = calculate_elo(winner_rating, loser_rating)

                rikishi_current_ratings[winner_id] = new_winner_rating
                rikishi_current_ratings[loser_id] = new_loser_rating

                # Store ratings for the current day
                if winner_id not in ratings_dict:
                    ratings_dict[winner_id] = {'ID': winner_id, 'Shikona': rikishi_info.at[winner_id, 'Shikona (EN)'],
                                               'Basho': basho, 'Division': row['Kubun']}
                ratings_dict[winner_id][f'{day}_rating'] = new_winner_rating

                if loser_id not in ratings_dict:
                    ratings_dict[loser_id] = {'ID': loser_id, 'Shikona': rikishi_info.at[loser_id, 'Shikona (EN)'],
                                              'Basho': basho, 'Division': row['Kubun']}
                ratings_dict[loser_id][f'{day}_rating'] = new_loser_rating

        # Save the ratings to a CSV file for the current basho (for testing purposes)
        basho_ratings = pd.DataFrame.from_dict(ratings_dict, orient='index')
        test_filename = f'../csvs/test/test_{basho}.csv'
        basho_ratings.to_csv(test_filename, index=False)
        print(f"{basho}場所終了")  # Print the completion of the current basho

    # Compile all ratings into a single DataFrame and save
    all_ratings = pd.DataFrame.from_dict(ratings_dict, orient='index')
    all_ratings.to_csv('../csvs/all_elorating.csv', index=False)


def main():
    basho_files = glob.glob('../csvs/matches_*.csv')
    rikishi_info = pd.read_csv('../csvs/rikishi_list.csv')
    rikishi_info.set_index('ID', inplace=True)

    process_basho_files(basho_files, rikishi_info)


if __name__ == '__main__':
    main()
