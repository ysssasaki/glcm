import numpy as np
##NSDを計算する関数
def calculate_nsd(current, historical):

    ##分子
    numerator = np.sum((current - historical)**2)
    ##分母
    denominator = (np.sum(current**2))**0.5 + (np.sum(historical**2))**0.5
    ##NSD
    nsd = numerator / denominator

    return float(nsd)

#RMSEを計算する関数
def calculate_rmse(x, y):
    ##引数x，yはndarray
    RMSE = (np.sum(x.astype(np.float64) - y.astype(np.float64))**2 / len(x))** 0.5

    return RMSE
