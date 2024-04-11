import requests
import csv

# Preparationクラスの定義
class Preparation:
    def __init__(self, basho):
        # 初期化メソッド。basho (場所) と階級のリストを保持。
        self.basho = basho
        self.divisions = [
            'Makuuchi', 'Juryo', 'Makushita',
            'Sandanme', 'Jonidan', 'Jonokuchi',
            'Maezumo', 'Others'
        ]

    # 指定された場所、日、階級に基づいて試合情報を取得するメソッド
    def get_matches_by_basho_and_day_and_division(self, day, division):
        # APIのURLを構築
        url = f'http://www.sumo-api.com/api/basho/{self.basho}/torikumi/{division}/{day}'
        # APIリクエストを送信
        response = requests.get(url)
        # レスポンスが成功した場合、試合情報をJSON形式で取得し、'torikumi'キーの内容を返す
        if response.status_code == 200:
            data = response.json()
            matches = data.get('torikumi')
            return matches
        else:
            # レスポンスが失敗した場合、Noneを返す
            return None

    # 取得した試合情報をCSVに保存するメソッド
    def save_matches_to_csv(self, matches, filename, division):
        # CSVファイルを追記モードで開く
        with open(filename, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # 各試合について行を書き込む
            for match in matches:
                writer.writerow([
                    match.get('id'), match.get('bashoId'), division,  # 各行に階級を含める
                    match.get('day'), match.get('matchNo'), match.get('eastId'),
                    match.get('eastShikona'), match.get('eastRank'), match.get('westId'),
                    match.get('westShikona'), match.get('westRank'), match.get('kimarite'),
                    match.get('winnerId'), match.get('winnerEn'), match.get('winnerJp')
                ])

    # 全階級、全日にわたって試合情報を取得し、CSVに保存するメソッド
    def record_all_matches(self):
        # CSVファイル名の設定（保存場所を相対パスで指定）
        filename = f'../csvs/matches_{self.basho}.csv'
        # CSVファイルを新規作成し、ヘッダー行を書き込む
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['ID', 'BashoId', 'Kubun', 'Day', 'MatchNo', 'EastId', 'EastShikona', 'EastRank', 'WestId',
                             'WestShikona', 'WestRank', 'Kimarite', 'WinnerId', 'WinnerEn', 'WinnerJp'])

        # 全階級、全日にわたって試合情報を取得し、CSVに保存
        days = range(1, 16)
        for division in self.divisions:
            for day in days:
                matches = self.get_matches_by_basho_and_day_and_division(day, division)
                if matches:
                    self.save_matches_to_csv(matches, filename, division)
# 年月を生成するための関数を定義
def generate_basho_list(start_year, end_year):
    months = ['01', '03', '05', '07', '09', '11']
    basho_list = []
    for year in range(start_year, end_year + 1):
        for month in months:
            basho_list.append(f'{year}{month}')
    return basho_list

# メイン処理
if __name__ == '__main__':
    # 1958年1月から2024年3月までのbashoリストを生成
    basho_list = generate_basho_list(1958, 2024)
    for basho in basho_list:
        prep = Preparation(basho)
        prep.record_all_matches()
