from numpy import *


def roadMeanVec(geohs, predictVecs):
    """ 计算整条路的平均速度 """
    vecs = roadVecs(geohs, predictVecs) # 获取所有速度信息
    meanVec = mean(vecs)    # 计算速度的平均速度
    maxVec = max(vecs)      # 计算速度的最大值
    minVec = min(vecs)      # 计算速度的最小值
    if meanVec > (maxVec + minVec)/2 :
        return meanVec
    else :
        return (maxVec + minVec)/2


def roadVecs(geohs, predictVecs):
    """ 获取该时刻还没走的路的速度 """
    vecs = []
    for geoh in geohs:
        vec = predictVecs[geoh][-1]
        vecs.append(vec)
    return vecs