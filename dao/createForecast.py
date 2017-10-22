from numpy import *
from utils.isExceptional import isExceptional
from utils.changeDate import changeDate, dateToTime


def isTree(obj):
    """ 判断该节点是否为叶子节点 """
    return (type(obj).__name__ == "dict")


def regTreeEval(model):
    """ 返回叶节点保存的值 """
    return float(model)


def dataForecast(tree, inData, modelEval=regTreeEval):
    """ 对单个数据进行预测 """
    if not isTree(tree): return modelEval(tree)     # 若为叶子节点，返回结果
    if inData[tree["spInd"]] <= tree["spVal"]:   # 小于等于分裂值，选择左子树
        if isTree(tree["left"]):    # 递归预测
            return dataForecast(tree["left"], inData, modelEval)
        else:       # 叶子节点，返回结果
            return modelEval(tree["left"])
    else:       # 大于分裂值，选择右子树
        if isTree(tree["right"]):
            return dataForecast(tree["right"], inData, modelEval)
        else:
            return modelEval(tree["right"])


def datasForecast(date, timeNow, geoh, test_datas, tree, modelEval=regTreeEval, timeBlock=6):
    """ 对数据集进行预测 """
    date = date.split("-")      # 分析当前日期
    year = int(date[0])
    month = int(date[1])
    day = int(date[2])
    timeNow = timeNow.split(":")    # 当前时间分析
    hour = int(timeNow[0])
    minute = int(timeNow[1])
    minute = minute - (minute % 6)

    time = dateToTime(year, month, day, hour, minute)   # 将时间进行整合

    exceps = []
    excepTimesInAnHour = 0  # 记录一个小时内异常发生次数
    tenTimesAnRound = 0  # 记录分析的时段次数，10次为一个轮回
    m = len(test_datas)   # 获取数据集个数
    for i in range(m):      # 循环对每个数据进行预测
        result = dataForecast(tree, test_datas[-(i+1)], modelEval)  # 预测结果
        isEX, e = isExceptional(time, result, test_datas[-(i+1)][-1], geoh)   # 异常情况判断
        if isEX :       # 有异常则进行保存
            excep = e
            tenTimesAnRound += 1  # 异常记录开始，连续记录10次
            excepTimesInAnHour += 1  # 一个小时异常发生次数
        elif tenTimesAnRound > 0:  # 异常分析已经开始
            tenTimesAnRound += 1  # 异常分析次数更新

        if tenTimesAnRound == 10:  # 从异常开始，连续分析满10个时间段
            if excepTimesInAnHour >= 6:  # 10次有6次发生异常则说明有异常
                excep["time"] = time  # 更新时间
                exceps.append(excep)
            tenTimesAnRound = 0  # 重置为0，重新分析异常
            excepTimesInAnHour = 0

        year,month,day,hour,minute = changeDate(year, month, day, hour, minute, timeBlock)  # 时间跳转
        time = dateToTime(year, month, day, hour, minute)   # 将时间进行整合
    return exceps





