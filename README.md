# sumo



俺が相撲データアナリストになるんだ！



## はじめに

Pythonは基本独学なので、変な書き方をしている可能性があります。

東大相撲部に所属し、Pythonをいじれる男として、野球のセイバーメトリクスのように相撲でも面白いデータ分析ができないかと思いました。

## データ成型: sumo_to_csvクラス

相撲レファレンスの表をPandas.Dataframeに落とし込み、CSVにします。
year, month, dayを渡す必要があります。
なお、

- year: 該当の西暦、int型
- month: 該当の月、str型(01みたいな形のため)。初場所なら```month == "01"```
- day: 何日目か、int型

なので注意。例として

```python
years = list(range(2010,2020)) #2010年から2019年まで
months = ["01", "03", "05", "07", "09", "11"]
days = list(range(1,16)) #1日目から15日目まで
for year in years:
    for month in months:
        for day in days:
            sumo = sumo_to_csv(year, month, day)
```

