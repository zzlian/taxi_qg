import json
from flask import Flask
from flask import request
from service.predictCarNum import predictCarNum
from service.predictCarNum import predictCarUseRatio
from service.predictDriveTime import predictDriveTime
from utils.hasException import hasException
from utils.isError import isError, isErrorInRatio, isErrorDriveTime
from utils.isModelBeenBuilt import readModelState

app = Flask(__name__)

@app.route("/predict/carnumber/block", methods=["POST"])
def carNumInBlock():
    """ 预测区域车辆数目 """
    req = request.json
    #req = json.loads(req)       # 将接受到的信息还原类型
    print(req)
    timeNow = req["timeNow"]    # 当前时间
    round = req["round"]        # 空出round个时间段不预测
    length = req["length"]      # 预测的时间段个数
    datas = req["data"]        # 区域中当前时间的前三个时间段的车辆数目
    print("出租车数量预测中....")
    if isError(datas) :       # 处理后台发送的错误信息
        predictDatas = {"state":13}
        return json.dumps(predictDatas)
    else :
        # try :
        predictDatas = predictCarNum(timeNow, round, length, datas, "block")  # 预测结果
        predictDatas["state"] = 1
        # except :
        #     predictDatas = {"state": 13}
        #     print("处理过程出错！！！")
        #     return json.dumps(predictDatas)
        print("预测成功！！！")
        return json.dumps(predictDatas)


@app.route("/predict/carnumber/singlepoint", methods=["POST"])
def carNumInSinglePoint():
    """ 预测单个区块的出租车流量变化趋势 """
    req = request.json
    print(req)
    #req = json.loads(req)
    timeNow = req["timeNow"]
    geohash = req["geohash"]
    round = req["round"]
    length = req["length"]
    numBef = req["numBef"]
    data = {geohash:numBef}
    print("正在预测出租车流量变化趋势....")
    if isError(data):       # 处理后台发送的错误信息
        predictDatas = {"state":13}
        return json.dumps(predictDatas)
    else :
        # try :
        predictDatas = predictCarNum(timeNow, round, length, data, "point") # 预测结果
        predictDatas["state"] = 1
        # except :
        #     predictDatas = {"state": 13}
        #     print("处理过程出错！！！")
        #     return json.dumps(predictDatas)
        print("预测成功！！！")
        return json.dumps(predictDatas)


@app.route("/predict/caruseratio", methods=["POST"])
def carUseRatio():
    """ 预测单个区块中车的利用率 """
    req = request.json
    print(req)
    #req = json.loads(req)
    timeNow = req["timeNow"]    # 当前时间
    geohash = req["geohash"]    # 对应的区块
    data = req["data"]
    numBef = data["numBef"]      # 总的车辆数目
    useBef = data["useBef"]      # 载客的车辆数目
    round = req["round"]        # 空出round个时间段不预测
    length = req["length"]      # 预测的时间段个数
    print("正在预测出租车利用率....")
    if isErrorInRatio(data, geohash) :
        predictDatas = {"state":13}
        return json.dumps(predictDatas)
    else :
        # try :
        predictDatas = predictCarUseRatio(timeNow, geohash, numBef, useBef, round, length)  # 预测结果
        predictDatas["state"] = 1
        # except :
        #     predictDatas = {"state": 13}
        #     print("处理过程出错！！！")
        #     return json.dumps(predictDatas)
        print("预测成功！！！")
        return json.dumps(predictDatas)


@app.route("/predict/drivetime", methods=["POST"])
def driveTime():
    """ 预测行程时间 """
    req = request.json
    print(req)
    #req = json.loads(req)
    timeNow = req["timeNow"]
    index = req["index"]    # 排好序的geohash
    data = req["data"]   # 多个区块的前三个时段的车辆速度
    err,num = isErrorDriveTime(data, index)
    print("正在预测出行路线的时间....")
    if err :
        predictTime = {"state":13}
        return json.dumps(predictTime)
    else :
        # try :
        predictTime = predictDriveTime(timeNow, index, data, num)  # 预测结果
        predictTime["state"] = 1
        # except :
        #     predictTime = {"state": 13}
        #     print("处理过程出错！！！")
        #     return json.dumps(predictTime)
        print("预测成功！！！")
        return json.dumps(predictTime)


@app.route("/exception", methods=["POST"])
def exception():
    """ 过去异常分析 """
    state = readModelState()     #获取建模状态
    print("异常请求....")
    if state["state"] == 13 :   #模型没建好，暂无异常分析
        print("模型还没建好！！！")
        return json.dumps(state)
    else:           #模型已经建好，异常分析完成
        result = {}
        exceps = hasException()
        result["state"] = 1
        result["exceptionPoints"] = exceps
        print("请求成功！！！")
        return json.dumps(result)


if __name__ == '__main__':
    app.run(host='localhost',port=10086)







