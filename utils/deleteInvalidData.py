from numpy import mean, array
import numpy as np


def deleteInvalidData(datas, error=10):
    """ 去除离群点 """
    result = datas[:]
    m = mean(array(datas)[:,-1])
    index = 0
    for data in datas :
        print(result)
        print(data)
        if (data[-1] - m) > error or (m - data[-1]) > error:
            np.delete(result, index, 0)
        index += 1
    return result