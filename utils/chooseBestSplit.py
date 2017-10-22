from numpy import *
from utils.binSplitDataSet import binSplitDataSet
from utils.deleteInvalidData import deleteInvalidData


def regLeaf(dataSet):
    """ 返回叶节点中数据的均值 """
    dataSet = array(dataSet)
    return mean(dataSet[:,-1])


def regErr(dataSet):
    """ 获取数据的总方差 """
    dataSet = array(dataSet)
    return var(dataSet[:,-1])*dataSet.shape[0]  # 算出均方差乘以数据个数


def chooseBestSplit(dataSet, leafType=regLeaf, errType=regErr, ops=(1,4)):
    """ 根据最小残差平方选择最佳分裂属性 """
    tolS = ops[0]; tolN = ops[1]    # 默认降低的最小总方差和最小数据量
    dataSet = array(dataSet)

    if len(set(dataSet[:,-1])) == 1:  # 判断节点中的数据是否属于同一类
        #dataSet = deleteInvalidData(dataSet)   # 删除数据中的离群点
        return None, leafType(dataSet)  # 若为同一类，返回数据标签的平均值

    m,n = dataSet.shape     # 获取数据集的行数和列数
    S = errType(dataSet)    # 计算数据集的总方差

    bestS = S; bestIndex = 0; bestValue = 0
    # 遍历每一个特征
    for featIndex in range(n-1):
        # 遍历特征的每一个取值
        for splitVal in set(dataSet[:,featIndex].tolist()):
            mat0,mat1 = binSplitDataSet(dataSet, featIndex, splitVal)   # 得到划分后的数据集
            if (mat0.shape[0] < tolN) or (mat1.shape[0] < tolN): continue   # 数据集不能小于默认阈值
            newS = errType(mat0) + errType(mat1)    # 获取划分后的总方差
            if newS < bestS:    # 选择具有较小方差的划分结果作为划分标准
                bestIndex = featIndex
                bestValue = splitVal
                bestS = newS

    if (S - bestS) < tolS:  # 划分后方差的差值不能小于默认阈值
        #dataSet = deleteInvalidData(dataSet)   # 删除数据中的离群点
        return None, leafType(dataSet)
    mat0,mat1 = binSplitDataSet(dataSet, bestIndex, bestValue)  # 获得最终划分结果
    if (mat0.shape[0] < tolN) or (mat1.shape[0] < tolN):    # 划分后数据集数目不能小于默认阈值
        #dataSet = deleteInvalidData(dataSet)    # 删除数据中的离群点
        return None, leafType(dataSet)
    return bestIndex, bestValue     # 返回最佳划分对应的特征索引和取值



