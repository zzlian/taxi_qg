import pickle
from dao.createForecast import datasForecast
from utils.hasException import hasException


def analyzeException(date, timeNow, train_datas, models, fileName=r"E:\taxi_datamining\qg_taxi_infos\exceps.txt"):
    """ 出租车流量异常分析 """
    exceps = hasException()     # 取出之前的异常情况进行整合
    for geoh in train_datas.keys():     # 分析异常
        excep = datasForecast(date, timeNow, geoh, train_datas[geoh], models[geoh]["numModel"])
        exceps.extend(excep)
    f = open(fileName, "wb")      # 将异常存进文件中
    pickle.dump(exceps, f)
    f.close()

