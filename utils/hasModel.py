import pickle
import os


def hasModel(fileName=r"E:\taxi_datamining\qg_taxi_infos\treeModels.txt"):
    """ 判断之前是否保存了训练模型 """
    isExist = os.path.isfile(fileName)
    if isExist :
        f = open(fileName, "rb")
        models = pickle.load(f)
        return models
    else : return {}