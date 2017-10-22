from numpy import *

def binSplitDataSet(dataSet, feature, value):
    """ 将数据集进行划分 """
    dataSet = array(dataSet)  # 转化为numpy array形式
    mat0 = dataSet[nonzero(dataSet[:,feature] <= value)[0],:]    # 特征值小于等于指定值
    mat1 = dataSet[nonzero(dataSet[:,feature] > value)[0],:]   # 特征值大于指定值
    return mat0,mat1