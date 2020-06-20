# -*- coding: utf-8 -*-

#以下の変数を設定して実行
target = "tomei"    ##対象路線(tomei or chuou)
gakushu = "shibuya" ##対応する学習路線(shibuya or shinjuku)
day = "18"          ##予測対象日
split_num = 3       ##分割個数(24を割り切れる数字で)
num_cand = 5        ##GLCMが類似している候補日・時間帯として抽出する個数

##############################################
import pandas as pd
import os
import pickle
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'IPAexGothic'
import time
import seaborn as sns
import csv
import read_data as rd
import glcm as gl
import function as fc
##############################################
path = os.getcwd()

time_step_list = []
time_num = 0
for i in range(split_num):
    next_time_num = int(time_num + 24/split_num)
    time_step_list.append(str(time_num) + "_" + str(next_time_num))
    time_num = next_time_num

area_name_list = ["shutoko", "nexco_naka"]
shuto_road_name_list = ["shibuya", "shinjuku"]
nexco_road_name_list = ["chuou", "tomei"]

for area_name in area_name_list:
    
    if area_name == "shutoko":
        road_name_list = shuto_road_name_list
        
    elif area_name == "nexco_naka":
        road_name_list = nexco_road_name_list

    for road_name in road_name_list:
    
        ##読み込むファイル名
        file_name = f"{road_name}.pickle"

        ##pickleファイルの読み込み
        with open(file_name, mode='rb') as f:
           df_list = pickle.load(f)
        
        ##分割後のdfの格納
        split_list = [[] for i in range(split_num)]
        
        ##分割(pandas.dataframeで格納)
        for df in df_list:
            for i in range(split_num):
                split_list[i].append(df.iloc[:,(24//split_num)*(i):(24//split_num)*(i+1)])
                
        time_num = 0
        for k in range(split_num):
            next_time_num = int(time_num + 24/split_num)
            dir_path = f"{time_num}_{next_time_num}_" + f"{road_name}"
            time_num = next_time_num
            pickle_list = []
            
            if area_name == "shutoko":
                for date in range(31):
                    df = split_list[k][date]
                    if not os.path.isdir(dir_path):
                        os.mkdir(dir_path)
                    out_file_name = dir_path + "_" + str(date) + ".csv"
                    df.to_csv(dir_path + "/" + out_file_name, index=False, header=None)
                    
            elif area_name == "nexco_naka":
                for date in range(31): 
                    df = split_list[k][date]
                    pickle_list.append(df)
                    
                with open(f"{dir_path}.pickle", 'wb') as f:
                    pickle.dump(pickle_list, f)


#main_func(road_name1,file_name1,int(24/split_num), time_step_list[p],day)
def main_func(road_name,fname,object_range,time_step,day):

    object_time = object_range - 1

    ##対象の日のタイムスペース図
    object_timespace = rd.Read_Data(fname)
    object_read_timespace = object_timespace.read_data()

    ##比較する日のタイムスペース図のファイルのリスト
    get_timespace_list = os.listdir(path+"/"+time_step+"_"+road_name)
    #get_timespace_list = os.listdir(road_name + "/"+time_step +"_"+road_name  )


    ##対象の日のglcm
    object_glcm = gl.GLCM(object_read_timespace)
    object_glcm_matrix = object_glcm.glcm(object_range, object_time)

    ##glcmを比較する
    nsd_dic = {}
    for file in get_timespace_list:
        file = time_step+"_"+road_name + "/" + file

        ##比較するタイムスペース図，glcmを作成する
        if fname != file:  
            get_timespace = rd.Read_Data(file)
            get_read_timespace = get_timespace.read_data()
            get_glcm = gl.GLCM(get_read_timespace)
            get_glcm_matrix = get_glcm.glcm(object_range, object_time)
    
            ##nsdを計算する
            nsd_val = fc.calculate_nsd(object_glcm_matrix, get_glcm_matrix)
            nsd_dic[file] = nsd_val
            
    sort_nsd = sorted(nsd_dic.items(), key = lambda x:x[1])
    ##5番目までの日付とnsdをリストに格納する
    list_day = []
    list_nsd = []
    for i in range(num_cand):
        list_day.append(sort_nsd[i][0])
        list_nsd.append(sort_nsd[i][1])
    
    dataf = pd.DataFrame()
    dataf["file"] = list_day
    dataf["nsd"] = list_nsd
    
    ##データを書き出す
    dataf.to_csv(road_name + time_step + "output" + str(day) + ".csv", index = False)



for p in range(len(time_step_list) - 1):   
    road_name1 = gakushu
    road_name2 = target
    file_name1 = time_step_list[p] + "_" + road_name1 + "/" + time_step_list[p] + "_" + road_name1 + "_" + str(day) + ".csv"
    main_func(road_name1,file_name1,int(24/split_num), time_step_list[p],day)

    ######### 中央道or東名道のデータ取得 ##############
    with open(time_step_list[p + 1] + "_" + road_name2 + ".pickle", mode='rb') as f:
        list_am = pickle.load(f)
    
    ######## output( 日付 と nsd )取得　「新宿」 ##############
    output = pd.read_csv(road_name1 + time_step_list[p] + "output" + str(day) + ".csv")
    
    ######## output から日付と重み結び付け 「新宿」　#################
    def Day_weight(output):
        day_omomi_list = output["file"].apply(lambda x : x.split("_")[-1][-6:-4])
        nsd = output["nsd"].values
        if sum(nsd):
            weight_list = nsd/sum(nsd)
        else:
            weight_list = [0.2] * 5
        return list(zip(day_omomi_list,weight_list))
    
    
    ######## 新宿線or渋谷線の日付と重みを中央道or東名道に結びつけて足し合わせる　###############
        
    day_weight_list = Day_weight(output)
    result_list =[]
    
    for day_weight in day_weight_list:
        day2 = day_weight[0]
        weight = day_weight[1]
        df_chuuou = list_am[int(day2)-1]
        weight_df = df_chuuou * weight
        weight_df.columns = list(map(lambda x: x.strftime("%H"), weight_df.columns)) 
        result_list.append(weight_df)
        
    df_heat = sum(result_list)
    vmin = 0
    vmax = 100
    ##時間計測
    t1 = time.time()
    fig, ax = plt.subplots(figsize=(5,7))
    sns.heatmap(df_heat,cmap="cool_r",ax=ax, vmin=vmin, vmax=vmax)
    ax.set_xticklabels(list(df_heat.columns))
    plt.xticks(rotation="horizontal")
    plt.yticks(rotation="horizontal")
    
    ##実行時間の出力
    t2 = time.time()
    elapsed_time = t2-t1
    print(f"実行時間：{elapsed_time}秒")

