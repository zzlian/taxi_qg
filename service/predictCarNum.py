from dao.changeToOneHot import changeToOneHot
from dao.createForecast import dataForecast
from dao.handleModels import getModels


def predictCarNum(timeNow, round, length, datas, predictType, timeBlock=6):
    """ 预测区域中总的车辆的数量 """
    models = getModels()    # 获取预测模型

    # 获取当前时间对应的one-hot编码
    oneHotNowIndex, timeNowIndex = changeToOneHot(timeNow, timeBlock)
    oneHotBlocks = (6*60) / 6    # 每个one-hot编码对应的时段个数

    predictDatas = {}       # 保存各个geohash中预测的值
    # 各个geohash中先预测出round个值
    for geoh in datas.keys():
        timeIndex = timeNowIndex
        oneHotIndex = oneHotNowIndex
        for i in range(round):
            model = models[geoh]["numModel"]    # 获取geohash对应的用于数量预测的模型
            if geoh not in predictDatas.keys():
                predictDatas[geoh] = datas[geoh]
            test_data = predictDatas[geoh][-3:]   # 前三个时段特征
            for i in range(4):      # 加对应时间的one-hot编码
                if i == oneHotIndex:
                    test_data.append(1)
                    continue
                test_data.append(0)
            predictData = int(dataForecast(model, test_data))  # 预测
            predictDatas[geoh].append(predictData)   # 将预测结果保存，可用于递归预测
            timeIndex += 1
            if timeIndex > oneHotBlocks:
                timeIndex = 1
                if oneHotIndex == 3: oneHotIndex = 0
                else: oneHotIndex += 1

    # 重新设置当前时间编码为round个时间段后的时间编码
    timeNowIndex = timeNowIndex + round
    if timeNowIndex > oneHotBlocks:
        timeNowIndex = timeNowIndex % oneHotBlocks
        if oneHotNowIndex == 3: oneHotNowIndex = 0
        else: oneHotNowIndex += 1

    # 预测各个geohash中接着的length个值
    for geoh in datas.keys():
        timeIndex = timeNowIndex
        oneHotIndex = oneHotNowIndex
        for i in range(length):
            model = models[geoh]["numModel"]    # 获取模型
            if geoh not in predictDatas.keys():
                predictDatas[geoh] = datas[geoh]
            test_data = predictDatas[geoh][-3:]
            for i in range(4):      # 加对应时间的one-hot编码
                if i == oneHotIndex:
                    test_data.append(1)
                    continue
                test_data.append(0)
            predictData = int(dataForecast(model, test_data)) # 进行预测
            predictDatas[geoh].append(predictData)
            timeIndex += 1
            if timeIndex > oneHotBlocks:
                timeIndex = 1
                if oneHotIndex == 3: oneHotIndex = 0
                else: oneHotIndex += 1

    if predictType == "block":  # 区域热力图预测
        result = {}
        gpsData = {}
        for geoh in datas.keys():
            if sum(predictDatas[geoh][-length:]) == 0:
                continue
            gpsData[geoh] = sum(predictDatas[geoh][-length:])
        result["gpsData"] = gpsData
        print(gpsData)
        return result
    else :          # 车流量趋势预测
        result = {}
        for geoh in datas.keys():
            result["predictFlow"] = predictDatas[geoh][-length:]
        print(result)
        return result


def predictCarUseRatio(timeNow, geohash, numBef, useBef, round, length, timeBlock=6):
    """ 预测单个geohash中车辆的利用率 """

    # 获取当前时间对应的one-hot编码
    oneHotIndex, timeIndex = changeToOneHot(timeNow, timeBlock)
    oneHotBlocks = (6 * 60) / 6  # 每个one-hot编码对应的时段个数

    models = getModels()
    numModel = models[geohash]["numModel"]
    usedNumModel = models[geohash]["usedNumModel"]

    # 预测出round个空轮回，用于递归预测
    for i in range(round):
        test_data = numBef[-3:]     # 前三个时段作为特征值
        for i in range(4):  # 加对应时间的one-hot编码
            if i == oneHotIndex:
                test_data.append(1)
                continue
            test_data.append(0)
        predictData = int(dataForecast(numModel, test_data)) # 预测
        numBef.append(predictData)
        test_data = useBef[-3:]
        for i in range(4):  # 加对应时间的one-hot编码
            if i == oneHotIndex:
                test_data.append(1)
                continue
            test_data.append(0)
        predictData = int(dataForecast(usedNumModel, test_data))
        useBef.append(predictData)
        timeIndex += 1
        if timeIndex > oneHotBlocks:
            timeIndex = 1
            if oneHotIndex == 3:
                oneHotIndex = 0
            else:
                oneHotIndex += 1

    # 预测需要用到的length个时间段的车辆数量
    for i in range(length):
        test_data = numBef[-3:]     # 前三个时间段作为特征值
        for i in range(4):  # 加对应时间的one-hot编码
            if i == oneHotIndex:
                test_data.append(1)
                continue
            test_data.append(0)
        predictData = int(dataForecast(numModel, test_data)) # 预测
        numBef.append(predictData)
        test_data = useBef[-3:]
        for i in range(4):  # 加对应时间的one-hot编码
            if i == oneHotIndex:
                test_data.append(1)
                continue
            test_data.append(0)
        predictData = int(dataForecast(usedNumModel, test_data))
        useBef.append(predictData)
        timeIndex += 1
        if timeIndex > oneHotBlocks:
            timeIndex = 1
            if oneHotIndex == 3:
                oneHotIndex = 0
            else:
                oneHotIndex += 1

    # 保存预测结果
    result = {}
    result["predictUse"] = sum(useBef[-length:])
    result["predictSum"] = sum(numBef[-length:])
    return result

