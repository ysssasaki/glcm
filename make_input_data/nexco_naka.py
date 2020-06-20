# -*- coding: utf-8 -*-
"""
Created on Mon Dec 17 10:35:35 2018

@author: sasaki
"""

import pandas as pd
import numpy as np
import time
import os
import calendar
import pickle


###########
###  設定
##対象年月
year = 2017
month = 8

##時間の集計単位
time_delta = "1h"

##KPの集計単位
kp_delta = 10

##状態量のカラム名
value_name = "速度"

##路線名のリスト
list_road_id = ["chuuou_kudari", "chuuou_nobori", "toumei_kudari", "toumei_nobori"]
list_name  =["中央道（下り）", "中央道（上り）", "東名（下り）", "東名（上り）"]

################
##時間のフォーマット変換
def jikan(year, month, day, time):
    return "{:04d}-{:02d}-{:02d} {}".format(year, month, day, time)


##インプットディレクトリへの移動
os.chdir(r"..\data\nexco_naka")

##時間計測
t1 = time.time()

##カラーマップの上限下限を設定
#vmin = min(df[value_name])
#vmax = max(df[value_name])
vmin = 0
vmax = 150

##路線ごとにインプットデータの作成を実行
for i in range(len(list_road_id)):
    road_id = list_road_id[i]
    name = list_name[i]
    
    ##データ読み込み
    df = pd.read_csv("{}.csv".format(road_id), encoding="SHIFT-JIS", header=1)
    
    ##NAを排除，データ型の変更
    df.dropna(how='all', inplace=True)
    df = df.astype({"年":int, "月":int, "日":int})
    
    ##時間の設定
    v_jikan = np.vectorize(jikan)
    list_jikan = v_jikan(df["年"], df["月"], df["日"], df["時刻"])
    df["datetime"] = list_jikan
    df["datetime"] = pd.to_datetime(df["datetime"])
    
    ##KPの集計
    list_cut = list(range(int(min(df["KP"]) // 10 * 10), int((max(df["KP"]) // kp_delta + 2)* kp_delta), kp_delta))
    df["cut"] = pd.cut(df["KP"], list_cut)
#    
    if not os.path.isdir(r"..\..\matrix\nexco_naka\{}".format(road_id)):
        os.makedirs(r"..\..\matrix\nexco_naka\{}".format(road_id))
    if not os.path.isdir(r"..\..\pickle\nexco_naka"):
        os.makedirs(r"..\..\pickle\nexco_naka")
    
    all_list = []

    ##集計
    for day in range(1, calendar.monthrange(year, month)[1]+1):##一日ずつで集計
        df_piv = pd.pivot_table(df, values=value_name,index="datetime",columns="cut")
        df_piv = df_piv[(df_piv.index.year == year) & (df_piv.index.month == month) & (df_piv.index.day == day)]
        
        ##時間の集計単位ごとに平均を算出
        df_heat = df_piv.groupby(pd.Grouper(freq=time_delta)).mean()
        df_heat = df_heat.T
        ##欠損は前後の平均で埋める
        df_heat = (df_heat.fillna(method="ffill").fillna(df_heat.fillna(method="bfill")) + df_heat.fillna(method="bfill").fillna(df_heat.fillna(method="ffill")))/2
        ##補完が正しくできているか確認
        print(len(df_heat) - len(df_heat.dropna()) == 0)
        all_list.append(df_heat)
        ##csvで出力
        df_heat.to_csv(r"..\..\matrix\nexco_naka\{0}\{0}_{1:02d}.csv".format(road_id,day), index=False, header=False)
    ##pickleで出力
    with open(r"..\..\pickle\nexco_naka\{}.pickle".format(road_id), mode='wb') as f:
        pickle.dump(all_list, f)


##実行時間の出力
t2 = time.time()
elapsed_time = t2-t1
print(f"実行時間：{elapsed_time}秒")