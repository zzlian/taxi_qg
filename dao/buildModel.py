from service.analyzeException import analyzeException
from utils.createTree import createTree
from utils.hasModel import hasModel
from dao.handleModels import storeModels


def transfArrToTrainData(timeStart, arr, timeBlock=6):
    """ 将数据列表转化为可进行建模的训练集 """

    # 设置时间的one-hot编码
    num = len(arr)      # 数据包含的时间段
    time = timeStart.split(":")
    hour = int(time[0])     # 当前小时
    minute = int(time[1])   # 当前分钟
    oneHotBlocks = (6*60)/6     # 编码对应的时间间隔数
    if hour >23 or hour <= 5:
        oneHotIndex = 0     # 该时段的one-hot编号
        if hour > 23: timeIndex = int(minute/timeBlock) # 对应与该编码区段的小时段
        else: timeIndex = 60/6 + int((hour*60+minute)/6)
    elif hour <= 11:
        oneHotIndex = 1
        timeIndex = int(((hour - 5)*60+minute)/6)
    elif hour <=17:
        oneHotIndex = 2
        timeIndex = int(((hour - 11)*60+minute)/6)
    else :
        oneHotIndex = 3
        timeIndex = int(((hour - 17)*60+minute)/6)

    # 将arr数组转换为训练集
    dataSet = []
    for i in range(num-3):
        data = arr[-(i+4):-(i+1)]       # 以前三个时段的数据作为特征值
        for j in range(4):      # 加时间one-hot编码
            if oneHotIndex == j:
                data.append(1)
                continue
            data.append(0)
        data.append(arr[-(i+1)])   # 对应类值
        dataSet.append(data)
        timeIndex -= 1
        if timeIndex <= 0 :     # 跳回上一个ont-hot编码对应的时段
            timeIndex = oneHotBlocks
            if oneHotIndex == 0: oneHotIndex = 3
            else: oneHotIndex -= 1
    return dataSet


def buildModel(timeStart, numArr, vecArr, useArr):
    """ 根据数据训练总车辆数量、载客车辆数量和速度模型 """

    # print("训练数组个数：", len(numArr))
    # print("对应出租车数量数组：",numArr)
    # print("对应速度数组：",vecArr)

    # 将数据列表转化为相应的训练集
    numArr = transfArrToTrainData(timeStart, numArr)
    vecArr = transfArrToTrainData(timeStart, vecArr)
    useArr = transfArrToTrainData(timeStart, useArr)

    # 训练相应的模型并保存在字典中
    model = {}
    model["numModel"] = createTree(numArr[:])
    print("build a numModel successfully")
    model["vecModel"] = createTree(vecArr)
    print("build a vecModel successfully")
    model["usedNumModel"] = createTree(useArr)
    print("build a usedNumModel successfully")
    return model, numArr


def buildModels(datas, timeStart, date, buildModelTime):
    """ 训练处各个区块的模型 """
    models = hasModel() #取出之前训练好的模型进行整合
    mods = {}

    train_datas = {}
    for data in datas:
        geohash = data["geohash"]    # 区块的geohash
        numArr = data["numArray"]    # 区块的车辆数量列表
        vecArr = data["vecArray"]    # 区块的速度列表
        useArr = data["useArray"]    # 区块的载客车辆数量列表
        model,train_data = buildModel(timeStart, numArr, vecArr, useArr)
        if buildModelTime == 1:
            train_datas[geohash] = train_data    # 保存对应geohash中的训练集
        else :
            print("训练集类型和个数：", type(train_data),len(train_data))
            train_datas[geohash] = train_data[240:]
        models[geohash] = model
        mods[geohash] = model
    # 将训练好的模型保存到文件中
    storeModels(models)
    # 异常分析
    print("...异常分析中...")
    if buildModelTime == 1 :
        print("第一次建立模型，分析所有异常....")
        analyzeException(date, timeStart, train_datas, mods)
    else :
        print("第"+str(buildModelTime)+"次建模，分析最近一天的异常....")
        analyzeException(date, timeStart, train_datas, mods)
    print("...异常分析结束...")