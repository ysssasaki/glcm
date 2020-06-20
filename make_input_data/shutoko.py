# -*- coding: utf-8 -*-
"""
Created on Tue Dec 18 10:31:42 2018

@author: sasaki
"""

import pandas as pd
import numpy as np
import time
import os
import datetime
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

##路線名のリスト
list_road_id = ["04-01", "04-02", "03-01", "03-02", "32-01", "32-02", "33-01", "33-02"]
list_files = ["201708_東京西地区②_区間QV.csv", "201708_東京西地区③_区間QV.csv",
              "201708_東京西地区④_区間QV.csv"]

##対象路線の設定
road_id ="04-01" ##新宿線


##カラーマップの上限下限を設定
#vmin = min(df[value_name])
#vmax = max(df[value_name])
vmin = 0
vmax = 80

##状態量のカラム名
value_name = "速度"
value_column = "V"

################


##インプットディレクトリへの移動
os.chdir(r"..\data\shutoko")

##時間計測
t1 = time.time()

##ファイルの読み込み
list_df = []
for v in list_files:
    df_tmp = pd.read_csv(v, header=[0,1], index_col=[0,1], engine="python")
    list_df.append(df_tmp)

##結合
df = pd.concat(list_df, axis=1)

##時間を集計しやすいように変換
def convert_to_datetime(d, t):
    ans = pd.to_datetime(d)
    str_ts = t[:5]
    str_te = t[-5:]
    ts = datetime.timedelta(hours=int(str_ts[:2]), minutes=int(str_ts[-2:]))
    te = datetime.timedelta(hours=int(str_te[:2]), minutes=int(str_te[-2:]))
    ti = (ts + te) / 2
    return ans + ti
v_convert_to_datetime = np.vectorize(convert_to_datetime)

list_time = list(zip(*df.index))
array_datetime = v_convert_to_datetime(list_time[0], list_time[1])
df.index = array_datetime


##対象道路の抽出
#road_id = list_road_id[0]
for road_id in list_road_id:
    
    ##出力ディレクトリへの移動
    if not os.path.isdir(r"..\..\matrix\shutoko\{}".format(road_id)):
        os.makedirs(r"..\..\matrix\shutoko\{}".format(road_id))
    if not os.path.isdir(r"..\..\pickle\shutoko".format(road_id)):
        os.makedirs(r"..\..\pickle\shutoko".format(road_id))

    ##対象路線を抽出
    list_columns = list(zip(*df.columns))[0]
    road_columns = [x for x in list_columns if x[:5].replace("‐","-") == road_id]
    
    all_list = []
    
    df_road = df.loc[:,(road_columns, value_column)]
    df_road.columns = list(zip(*df_road.columns))[0]
    for day in range(1, calendar.monthrange(year, month)[1]+1):
        df_road_day = df_road[(df_road.index.year == year) & (df_road.index.month == month) & (df_road.index.day == day)]
        
        ##時間の集計単位ごとに平均を算出
        df_heat = df_road_day.groupby(pd.Grouper(freq=time_delta)).mean()
        df_heat = df_heat.T
        ##欠損は前後の平均で埋める
        df_heat = (df_heat.fillna(method="ffill").fillna(df_heat.fillna(method="bfill")) + df_heat.fillna(method="bfill").fillna(df_heat.fillna(method="ffill")))/2
        ##補完が正しくできているか確認
        print(len(df_heat) - len(df_heat.dropna()) == 0)
        ##csvで出力
        df_heat.to_csv(r"..\..\matrix\shutoko\{0}\{0}_{1:02d}.csv".format(road_id,day), index=False, header=False)
        all_list.append(df_heat)
    
    ##pickleで出力 
    with open(r"..\..\pickle\shutoko\{}.pickle".format(road_id), mode='wb') as f:
        pickle.dump(all_list, f)
    


##実行時間の出力
t2 = time.time()
elapsed_time = t2-t1
print(f"実行時間：{elapsed_time}秒")