import pandas as pd
import os


def find_top_ten(directory):
    highest_ratings = pd.DataFrame()

    # ディレクトリ内のすべてのCSVファイルを走査
    for filename in os.listdir(directory):
        if filename.startswith('test_') and filename.endswith('.csv'):
            filepath = os.path.join(directory, filename)
            basho = filename.split('_')[1].split('.')[0]
            df = pd.read_csv(filepath)

            # 各日のレーティング列を走査
            for day in range(1, 16):
                day_rating_column = f'{day}_rating'
                if day_rating_column in df.columns:
                    df_day = df[['ID', 'Shikona']].copy()
                    df_day['Basho'] = basho
                    df_day['Day'] = day
                    df_day['Rating'] = df[day_rating_column]

                    # 現在のデータに対して最高レーティングのみを保持
                    highest_ratings = pd.concat([highest_ratings, df_day])
                    highest_ratings = highest_ratings.sort_values(by=['ID', 'Rating'],
                                                                  ascending=[True, False]).drop_duplicates(subset='ID',
                                                                                                           keep='first')

    # 全データの中からトップ10を選出
    highest_ratings.sort_values(by='Rating', ascending=False, inplace=True)
    top_ten = highest_ratings.head(10)
    top_ten.to_csv(os.path.join(directory, 'top_ten.csv'), index=False)
    print("Top 10 ratings saved to top_ten.csv")

find_top_ten('../csvs/test')
