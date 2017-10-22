import pickle
import os


def getModels(fileName=r"E:\taxi_datamining\qg_taxi_infos\treeModels.txt"):
    """ 取出预测模型 """
    f = open(fileName, "rb")
    models = pickle.load(f)  # 取出事先训练好的模型
    f.close()
    return models


def storeModels(models, fileName=r"E:\taxi_datamining\qg_taxi_infos\treeModels.txt"):
    """ 将训练好的模型保存到文件中 """
    f = open(fileName, "wb")
    pickle.dump(models, f)
    f.close()


def getBuildModelTime(fileName=r"E:\taxi_datamining\qg_taxi_infos\buildModelTime.txt"):
    """ 记录模型建立的次数 """
    isExist = os.path.isfile(fileName)
    if isExist :
        f = open(fileName, "rb")
        time = pickle.load(f)
        f.close()
        return time["time"]
    else :
        return 0


def setBuildModelTime(buildTime, fileName=r"E:\taxi_datamining\qg_taxi_infos\buildModelTime.txt"):
    """ 保存模型建立的次数 """
    time = {"time": buildTime}
    f = open(fileName, "wb")
    pickle.dump(time, f)
    f.close()