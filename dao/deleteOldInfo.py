import os


def deleteOldModel(fileName=r"E:\taxi_datamining\qg_taxi_infos\treeModels.txt"):
    """ 重新建模时，删除之前的建好的模型 """
    isExist = os.path.isfile(fileName)
    if isExist :  os.remove(fileName)


def deleteOldExceps(fileName=r"E:\taxi_datamining\qg_taxi_infos\exceps.txt"):
    """ 重新建模时清空之前的异常情况 """
    isExist = os.path.isfile(fileName)
    if isExist : os.remove(fileName)