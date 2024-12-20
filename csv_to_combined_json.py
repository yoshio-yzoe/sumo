import csv
import json
import os

def read_rikishi_list(csv_file_path):
    rikishi_list = []
    with open(csv_file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rikishi_list.append(row)
    return rikishi_list

def read_ratings(csv_dir):
    ratings = []
    for filename in os.listdir(csv_dir):
        if filename.startswith('rating_') and filename.endswith('.csv'):
            csv_path = os.path.join(csv_dir, filename)
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    rating_entry = {
                        "RikishiID": row["RikishiID"],
                        "Shikona": row["Shikona"],
                        "Basho": row["Basho"],
                        "ratings": []
                    }
                    for day in range(1, 16):
                        rating_key = f"{day}_rating"
                        rating_value = row.get(rating_key, "1500")
                        try:
                            rating_entry["ratings"].append(int(rating_value))
                        except ValueError:
                            rating_entry["ratings"].append(1500)  # デフォルト値
                    ratings.append(rating_entry)
    return ratings

def read_matches(csv_dir):
    matches = []
    for filename in os.listdir(csv_dir):
        if filename.startswith('matches_') and filename.endswith('.csv'):
            csv_path = os.path.join(csv_dir, filename)
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    matches.append(row)
    return matches

def convert_to_combined_json(rikishi_csv, rating_dir, matches_dir, output_json):
    combined_data = {}
    
    # 力士リストの読み込み
    print("Reading rikishi list...")
    combined_data["rikishi_list"] = read_rikishi_list(rikishi_csv)
    
    # レーティングデータの読み込み
    print("Reading ratings...")
    combined_data["ratings"] = read_ratings(rating_dir)
    
    # 試合データの読み込み
    print("Reading matches...")
    combined_data["matches"] = read_matches(matches_dir)
    
    # JSONに書き出し
    print(f"Writing combined data to {output_json}...")
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(combined_data, f, ensure_ascii=False, indent=4)
    
    print("Conversion completed.")

if __name__ == "__main__":
    # パスの設定
    rikishi_csv = os.path.join('csvs', 'rikishi_list.csv')
    rating_dir = os.path.join('csvs', 'rating')
    matches_dir = os.path.join('csvs')
    output_json = os.path.join('data', 'combined_data.json')
    
    # 出力ディレクトリの作成
    os.makedirs('data', exist_ok=True)
    
    # 変換の実行
    convert_to_combined_json(rikishi_csv, rating_dir, matches_dir, output_json)
