# 相撲の力士のレーティング算出
番付が実際の実力と乖離して久しく、ここに力士の実際の実力を計るべくレーティングの実装を試みる。

## レーティングとは
イロレーティング（Elo rating）は、プレイヤーの相対的なスキルレベルを数値化するために使用されるシステムである。<br>
これを相撲に応用するためには、まず各力士の勝敗データを基にレーティングを計算し、その後、新たな試合の結果が出るたびにレーティングを更新していく必要がある。

### イロレーティングの計算ステップ

1. **初期レーティングの設定**: 全ての力士に対して、初期レーティング（1500）を設定
2. **レーティングの更新**: 試合が行われるたびに、以下のステップを用いて両力士のレーティングを更新
   - **勝者の期待スコアの計算**: <img src="https://latex.codecogs.com/svg.image?E_A=\frac{1}{1&plus;10^{(R_B-R_A)/400}}\"/>
   - **敗者の期待スコアの計算**: <img src="https://latex.codecogs.com/svg.image?&space;E_B=\frac{1}{1&plus;10^{(R_A-R_B)/400}}\"/>
   - **レーティングの更新**: 勝者の新しいレーティング <img src="https://latex.codecogs.com/svg.image?&space;R'_A=R_A&plus;K(S_A-E_A)"/>、敗者の新しいレーティング <img src="https://latex.codecogs.com/svg.image?R'_B=R_B&plus;K(S_B-E_B)"/> ここで、<img src="https://latex.codecogs.com/svg.image?R_A"/> と <img src="https://latex.codecogs.com/svg.image?R_B"/> は試合前のレーティング、<img src="https://latex.codecogs.com/svg.image?S_A"/> と <img src="https://latex.codecogs.com/svg.image?S_B"/> は試合の結果（勝者は1、敗者は0）、<img src="https://latex.codecogs.com/svg.image?K"/> は定数（一般的には16または32）。

### 相撲データAPIを利用した実装

このAPIを利用して、力士のイロレーティングを測定するためには、主に `GET /api/rikishi/:rikishiId/matches` エンドポイントを使用して、各力士の試合結果を取得する。

1. **力士情報の取得**: `GET /api/rikishis` エンドポイントを使って、必要な力士の情報（特に `rikishiId`）を取得。
2. **試合結果の取得**: 各力士について `GET /api/rikishi/:rikishiId/matches` を使って、その力士のすべての試合結果を取得。
3. **イロレーティングの計算**: 取得した試合結果に基づいて、上記のステップに従って各力士のイロレーティングを計算。
4. **レーティングの更新**: 新たな試合結果が出るたびに、対応する力士のレーティングを更新。

なのでイロレーティングシステムを相撲に適用する場合、
過去のある時点（今回は1958年1月場所）から全力士のレーティングを初期値1500に設定し、
そこから各日に行われる試合の結果に基づいて力士のレーティングを更新していく必要がある。

具体的な手順は以下の通り。

1. **初期レーティングの設定**: 
   - 指定した開始点（1958年1月場所）で全力士のイロレーティングを1500と設定。

2. **日々の試合結果に基づく更新**:
   - 各場所の各日における全ての試合結果を取得。
   - 当日に試合を行う各力士のペアごとに、前述したイロレーティングの計算式に従ってレーティングを更新。
   - このプロセスをその場所の全ての日に対して繰り返し、次に移る。

3. **レーティングの記録と更新**:
   - 各力士のレーティングは日々更新され、これらの変化をデータベースやファイルシステムに記録。
   - 次の場所が始まる前に、最新のレーティングを基点として再び更新を開始する。

