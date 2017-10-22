from utils.chooseBestSplit import *

def createTree(dataSet, leafType=regLeaf, errType=regErr, ops=(1,4)):
    """ 递归生成回归决策树 """
    feat, val = chooseBestSplit(dataSet, leafType, errType, ops) # 选择最佳划分特征
    if feat == None: return val     # 若没有最佳划分特征，则作为叶子节点返回
    retTree = {}    # 用字典来保存树结构
    retTree["spInd"] = feat     # 划分特征对应的索引
    retTree["spVal"] = val      # 特征对应的划分值
    lSet, rSet = binSplitDataSet(dataSet, feat, val)    # 根据特征将数据集进行划分
    retTree["left"] = createTree(lSet, leafType, errType, ops)   # 递归生成左子树
    retTree["right"] = createTree(rSet, leafType, errType, ops)   # 递归生成右子树
    return retTree