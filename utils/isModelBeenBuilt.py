import pickle
import os


def deleteState(fileName=r"E:\taxi_datamining\qg_taxi_infos\buildModel.txt"):
    """ 重新建模，删除状态码 """
    isExist = os.path.isfile(fileName)
    if isExist : os.remove(fileName)


def modelBeenBuilt(fileName=r"E:\taxi_datamining\qg_taxi_infos\buildModel.txt"):
    """ 保存建好模的状态码 """
    state = {"state":1}
    f = open(fileName, "wb")
    pickle.dump(state, f)
    f.close()


def readModelState(fileName=r"E:\taxi_datamining\qg_taxi_infos\buildModel.txt"):
    """ 读取建模状态 """
    isExist = os.path.isfile(fileName)
    if not isExist :            #还没建好模，state为13
        state = {"state":13}
        return state
    else :                      #建完模，state为1
        state = {"state":1}
        return state
