import os
import pickle


def hasException(fileName=r"E:\taxi_datamining\qg_taxi_infos\exceps.txt"):
    """ 判断之前是否保存了异常情况 """
    isExist = os.path.isfile(fileName)
    if isExist:
        f = open(fileName, "rb")
        exceps = pickle.load(f)
        return exceps
    else:
        return []