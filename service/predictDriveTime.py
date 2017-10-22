from dao.changeToOneHot import changeToOneHot
from dao.createForecast import dataForecast
from dao.handleModels import getModels
from utils.roadMeanVec import roadMeanVec


def predictDriveTime(timeNow, orderedgeohashs, geohashs, errNum, distance=0.076, timeBlock=6):
    """ 预测出行路程所需的时间 """

    print("geohash不存在的个数：",errNum)
    geohNum = errNum + len(orderedgeohashs)

    # 获取当前时间对应的one-hot编码
    oneHotIndex, timeIndex = changeToOneHot(timeNow, timeBlock)
    oneHotBlocks = (6 * 60) / 6  # 每个one-hot编码对应的时段个数

    models = getModels()    # 获取模型
    geohashToPredict = orderedgeohashs[:]   # 保存待预测的geohash
    timeToSpend = 0.0   # 行程花费时间
    timeSpended = 0.0     # 记录时间花费是否大于15minutes

    # 保存geohash对应的速度时间序列
    predictVecs = {}
    for geoh in orderedgeohashs:
        predictVecs[geoh] = geohashs[geoh]

    while True:
        if not geohashToPredict:
            break
        # 预测对应geohash中的速度
        for geoh in orderedgeohashs:
            model = models[geoh]["vecModel"]  # 获取预测速度的模型
            test_data = predictVecs[geoh][-3:]
            for i in range(4):      # 加对应时间的one-hot编码
                if i == oneHotIndex:
                    test_data.append(1)
                    continue
                test_data.append(0)
            predictVec = dataForecast(model, test_data)  # 预测速度
            predictVecs[geoh].append(predictVec)
        timeIndex += 1
        if timeIndex > oneHotBlocks:    # one-hot编码的时间间隔数不能超过oneHotBlocks
            timeIndex = 1
            if oneHotIndex == 3:
                oneHotIndex = 0
            else:
                oneHotIndex += 1
        # 计算时间
        meanVec = roadMeanVec(orderedgeohashs, predictVecs)
        for geoh in orderedgeohashs:
            #if predictVecs[geoh][-1] == 0 : break   #速度为0时，重新进行预测
            if meanVec == 0 : break     # 平均速度为0，重新进行预测
            #timeSpended += (distance / float(predictVecs[geoh][-1]))*60.0  # 计算走过多个geohash耗费的时间
            timeSpended += (distance / float(meanVec))*60.0     # 计算走过多个geohash耗费的时间
            print("时间：",timeSpended, "速度：", meanVec)
            if timeSpended >= timeBlock:  # 若前面geohash耗费时间超过一个时段，则后面geohash的速度需再次预测
                geohashToPredict.remove(geoh)
                break
            geohashToPredict.remove(geoh)
        timeToSpend += timeSpended    # 行程耗费时间
        timeSpended = 0.0
        orderedgeohashs = geohashToPredict[:]   # 待预测geohashs

    # 计算到达的时间
    timeToSpend += errNum*0.2 + geohNum/5
    hours = int(timeToSpend / 60)
    minute = int(timeToSpend) % 60
    time = timeNow.split(":")
    hours = hours + int(time[0])
    minute = minute + int(time[1])
    if minute >= 60:
        hours += 1
        minute = minute % 60
    if minute < 10 : minute = "0" + str(minute)
    time = str(hours) + ":" + str(minute)

    # 将到达时间和行程耗费时间保存
    result = {}
    result["predictTime"] = time
    if timeToSpend < 1:
        result["driveTime"] = 1
    else :
        result["driveTime"] = int(timeToSpend)
    return result