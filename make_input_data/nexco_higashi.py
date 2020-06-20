# -*- coding: utf-8 -*-
"""
Created on Thu Jan 24 13:51:36 2019

@author: sasaki
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#import matplotlib.dates as mdates
plt.rcParams['font.family'] = 'IPAexGothic'
plt.switch_backend('Agg')
import time
import os
#import datetime
import calendar

import pickle


###########
###  設定
year = 2017
month = 8
day = 1

time_delta = "1h"

kp_delta = 10

##状態量

value_name = "速度"

################


##ディレクトリの移動
os.chdir(r"..\data\nexco_higashi")

##時間計測
t1 = time.time()

##データ読み込み
##圏央道
##8月
df = pd.read_csv("2.csv", encoding="SHIFT-JIS", header=1)
##10月
#df = pd.read_csv("25.csv", encoding="SHIFT-JIS", header=1)
name = "圏央道"
road_id = "kennoudou"

##時間の設定
def jikan(year, month, day, time):
    return "{:04d}-{:02d}-{:02d} {}".format(year, month, day, time)
v_jikan = np.vectorize(jikan)
list_jikan = v_jikan(df["年"], df["月"], df["日"], df["時刻"])
df["datetime"] = list_jikan
df["datetime"] = pd.to_datetime(df["datetime"])

##KPの集計
list_cut = list(range(int(min(df["KP"]) // 10 * 10), int((max(df["KP"]) // kp_delta + 2)* kp_delta), kp_delta))
df["cut"] = pd.cut(df["KP"], list_cut)


##カラーマップの上限下限を設定
#vmin = min(df[value_name])
#vmax = max(df[value_name])
vmin = 0
vmax = 150

if not os.path.isdir(r"..\..\matrix\nexco_higashi\{}".format(road_id)):
    os.makedirs(r"..\..\matrix\nexco_higashi\{}".format(road_id))
if not os.path.isdir(r"..\..\pickle\nexco_higashi"):
    os.makedirs(r"..\..\pickle\nexco_higashi")

all_list = []

##集計
for day in range(1, calendar.monthrange(year, month)[1]+1):
    df_piv = pd.pivot_table(df, values=value_name,index="datetime",columns="cut")
    df_piv = df_piv[(df_piv.index.year == year) & (df_piv.index.month == month) & (df_piv.index.day == day)]
    
    df_heat = df_piv.groupby(pd.Grouper(freq=time_delta)).mean()
    df_heat = df_heat.T
    ##欠損は前後の平均で埋める
    df_heat = (df_heat.fillna(method="ffill").fillna(df_heat.fillna(method="bfill")) + df_heat.fillna(method="bfill").fillna(df_heat.fillna(method="ffill")))/2
    ##補完が正しくできているか確認
    print(len(df_heat) - len(df_heat.dropna()) == 0)
    all_list.append(df_heat)
    break
    ##csvで出力
#    df_heat.to_csv(r"..\..\matrix\nexco_higashi\{0}\{0}_{1:02d}.csv".format(road_id,day), index=False, header=False)
###pickleで出力
#with open(r"..\..\pickle\nexco_higashi\{}.pickle".format(road_id), mode='wb') as f:
#    pickle.dump(all_list, f)
        
    