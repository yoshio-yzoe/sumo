import requests
import csv
import time


def fetch_all_rikishi_data():
    """
    sumo-api.comから全ての力士データを取得する関数。
    ページネーションを利用して複数回のリクエストを行う。

    戻り値:
    - list: 全ての力士データを含むリスト。
    """
    base_url = 'https://www.sumo-api.com/api/rikishis'
    params = {'intai': 'true', 'limit': 1000, 'skip': 0}
    all_rikishis = []

    while True:
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()

            rikishis = data.get('records', [])
            all_rikishis.extend(rikishis)

            print(f"Retrieved {len(rikishis)} rikishi records. Total: {len(all_rikishis)}")

            if len(rikishis) < params['limit']:
                break  # 取得したレコード数が limit より少ない場合、全データを取得済みと判断

            params['skip'] += params['limit']  # 次のページへ
            time.sleep(1)  # APIへの負荷を軽減するため、リクエスト間に1秒の待機を入れる

        except requests.RequestException as e:
            print(f"Error fetching rikishi data: {e}")
            break

    print(f"Total rikishi records retrieved: {len(all_rikishis)}")
    return all_rikishis


def save_rikishi_data_to_csv(rikishis, filename='../csvs/rikishi_list.csv'):
    """
    取得した力士データをCSVファイルに保存する関数。
    力士IDの昇順でソートし、欠損データがある場合も行を作成する。

    引数:
    - rikishis: 力士データのリスト
    - filename: 保存先のCSVファイル名
    """
    # 力士IDでソート
    sorted_rikishis = sorted(rikishis, key=lambda x: int(x.get('id', 0)))

    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ['ID', 'SumoDB ID', 'NSK ID', 'Shikona (EN)', 'Shikona (JP)', 'Heya', 'Birth Date', 'Shusshin',
                      'Debut', 'Intai', 'Updated At']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for rikishi in sorted_rikishis:
            row = {
                'ID': rikishi.get('id', ''),
                'SumoDB ID': rikishi.get('sumodbId', ''),
                'NSK ID': rikishi.get('nskId', ''),
                'Shikona (EN)': rikishi.get('shikonaEn', ''),
                'Shikona (JP)': rikishi.get('shikonaJp', ''),
                'Heya': rikishi.get('heya', ''),
                'Birth Date': rikishi.get('birthDate', ''),
                'Shusshin': rikishi.get('shusshin', ''),
                'Debut': rikishi.get('debut', ''),
                'Intai': rikishi.get('intai', ''),
                'Updated At': rikishi.get('updatedAt', '')
            }
            writer.writerow(row)

    print(f"Saved {len(sorted_rikishis)} rikishi records to {filename}")


def main():
    """
    メイン処理関数。
    力士データの取得とCSVファイルへの保存を行う。
    """
    rikishis = fetch_all_rikishi_data()
    if rikishis:
        save_rikishi_data_to_csv(rikishis)
    else:
        print("No rikishi data available or error occurred during data retrieval.")


if __name__ == "__main__":
    main()