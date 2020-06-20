# -*- coding: utf-8 -*-
"""
Created on Thu Dec 27 17:06:29 2018

@author: sasaki

分割結果　→　split_list

例）
split[0][2]　→　分割インデックス0の日付インデックス2
三分割の場合　2017-08-03 00:00:00' ~　'2017-08-03 07:00:00'

"""

import pandas as pd
import os
import pickle


##############################################

##inputのパス
path = r"D:\sasa\master\data_challenge\input_data\pickle\shutoko"

##読み込むファイル名
file_name = "04-01.pickle"

##分割個数(24を割り切れる数字で)
split_num = 3

#############################################

##インプットフォルダへの移動
os.chdir(path)

##pickleファイルの読み込み
with open(file_name, mode='rb') as f:
   df_list = pickle.load(f)

##分割後のdfの格納
split_list = [[] for i in range(split_num)]

##分割(pandas.dataframeで格納)
for df in df_list:
    for i in range(split_num):
        split_list[i].append(df.iloc[:,(24//split_num)*(i):(24//split_num)*(i+1)])



###分割(numpy.arrayで格納)
#for df in df_list:
#    for i in range(split_num):
#        split_list[i].append(df.iloc[:,(24//split_num)*(i):(24//split_num)*(i+1)].values)