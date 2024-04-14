import csv
import requests

def fetch_all_rikishi_data():
    url = 'http://www.sumo-api.com/api/rikishis?intai=true'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        rikishis = data.get('records')
        if rikishis:
            # 最初の数件の力士データをプリントアウトする
            print(rikishis[:5])
            return rikishis
        else:
            print("Error: 'records' key not found or is empty.")
            return []
    else:
        print(f"Failed to fetch rikishi data: HTTP {response.status_code}")
        return []

# データの取得とプリントアウト
rikishis = fetch_all_rikishi_data()



def save_rikishi_data_to_csv(rikishis, filename='../csvs/rikishi_list.csv'):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['ID', 'SumoDB ID', 'NSK ID', 'Shikona (EN)', 'Heya', 'Birth Date', 'Shusshin', 'Debut', 'Intai', 'Updated At'])
        for rikishi in rikishis:
            # デバッグ出力: 書き込む力士データを表示
            print(f"Writing rikishi data to CSV: {rikishi}")
            writer.writerow([
                rikishi.get('id'), rikishi.get('sumodbId'), rikishi.get('nskId'),
                rikishi.get('shikonaEn'), rikishi.get('heya'), rikishi.get('birthDate'),
                rikishi.get('shusshin'), rikishi.get('debut'), rikishi.get('intai'),
                rikishi.get('updatedAt')
            ])

# 使用例
filename = 'rikishi_data.csv'
save_rikishi_data_to_csv(rikishis, filename)



# メイン処理
rikishis = fetch_all_rikishi_data()
if rikishis:
    save_rikishi_data_to_csv(rikishis)
else:
    print("No rikishi data available.")
