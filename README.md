# 概要

- GLCM(gray level co-occurrence matrix)を用いた画像認識による高速道路の渋滞予測
- 参考文献
  - Hall-Beyer, Mryka. "GLCM texture: a tutorial." National Council on Geographic Information and Analysis Remote Sensing Core Curriculum 3 (2000).
  - Zhang, Zhihao, et al. "Probe data-driven travel time forecasting for urban expressways by matching similar spatiotemporal traffic patterns." Transportation Research Part C: Emerging Technologies 85 (2017): 476-493.
- 土木学会インフラデータチャレンジにて発表(http://committees.jsce.or.jp/cceips17/node/12)


# 説明

## 説明資料(.pptx)
https://drive.google.com/open?id=1FaEzoX5fuI5ogpnFaJVqECJeBELwFayW

## 画像を作成するためのデータセット(削除済み)
- chuou.pickle
- tomei.pickle
- shibuya.pickle
- shinjuku.pickle

## pythonファイル一覧
1. main.py
2. glcm.py
3. function.py
4. read_data.py

### 1. main.py
実行するメインファイル
設定する変数は以下の通り
- target：対象路線を指定
- gakushu：対応する学習路線
- day：予測対象日
- split_num：分散個数
- num_cand：類似している候補日・時間帯として抽出する個数

### 2. glcm.py
glcmのクラス：タイムスペース図をマトリクスに変換する

### 3. function.py
glcm内で使用する関数

### 4. read_data.py
csvを読み込むためのクラス：glcmクラスとともに使用

## 実行
main.pyを実行することで，ある特定の日における
首都高速道路の新宿から，ネクスコ中日本の中央道，
首都国則道路の渋谷から，ネクスコ東名道の道路の将来の状態をあてる．
