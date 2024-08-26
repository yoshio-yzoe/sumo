# sumo data analysis

俺が相撲データアナリストになるんだ！

## はじめに

Pythonは基本独学なので、変な書き方をしている可能性があります。

東大相撲部に所属し、Pythonをいじれる男として、野球のセイバーメトリクスのように相撲でも面白いデータ分析ができないかと思いました。

## 本題

### データ整形
まずデータベース作成が必要である。

以下の実行により、指定された場所における全ての階級、全日にわたる試合情報を取得し、`csvs`ディレクトリ内にCSVファイルとして保存する。<br>
CSVファイルには、試合ID、場所ID、階級、日、試合番号、東側力士のIDと四股名と番付、西側力士のIDと四股名と番付、決まり手、勝者のID、勝者の英語名、勝者の日本語名が含まれる。
```commandline
$ python3 make_database.py <start_year> <end_year>
```
例として、2000~2020年真で保存する場合は
```commandline
$ python3 make_database.py 2000 2020
```
デフォルトでは1958年以降の全場所のデータを保存するので、必要であれば`if __name__ == '__main__':`以下の`basho`(YYYYMM形式)を編集すると、指定した場所のCSVが作られる。

### レーティング計算
これを使って力士のレーティングを作ってみようかなと思う。(詳しくは`elo_rating.md`参照)<br>
以下の実行により`csvs/rating`ディレクトリの中に力士ID、四股名、場所、各日のレーティングが記載されるCSV、`rating<year><month>.csv`が保存される。
```commandline
$ python3 elo_rating.py
```
また、以下の実行により歴代のトップレーティング歴史を保存かつ表示できる。
```commandline
$ python3 top_rating.py 10
```
上記の例では、トップ10の力士のレーティングデータが`../csvs/rating/top_10_ratings.csv`に保存され、同時にターミナルに結果が表示される。

### 最新データへのUpgrade
以下の実行により、make_database.pyとelo_rating.pyが共に最新版まで実行される。
```commandline
$ python3 update.py
```

## old
昔は全然違うやり方してたんで、そちらは昔のコミットを参照
（当時はSumo-APIがなかったので、Sumo Referenceよりスクレイピングしていました）


