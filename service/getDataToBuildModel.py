from dao.buildModel import buildModels
from dao.getFiveBitGeoh import getFiveBitGeohs
from dao.deleteOldInfo import deleteOldModel, deleteOldExceps
from utils.isModelBeenBuilt import modelBeenBuilt, deleteState
from dao.handleModels import getBuildModelTime, setBuildModelTime
import json
import requests


def getDataToBuildModel(geohashs, buildModelTime):
    """ 向后台请求数据进行建模 """
    #  测试  "ws0df","ws0ed","ws0eh","ws0e6","ws0ed","ws0e9","ws0ef"
    num = 0
    # requestTimes = len(geohashs)
    # requestTime = 0

    for geoh in geohashs :
        # requestTime +=1
        num += 1
        if num == 2 : break
        headers = {'content-type': 'application/json'}
        data = {"geoHashs":[geoh]}
        data["buildModelTime"] = str(buildModelTime)
        # if requestTime == requestTimes :
        #     data["buildModelTime"] = str(buildModelTime + 1)
        # else :
        #     data["buildModelTime"] = str(buildModelTime)
        print("time:",data["buildModelTime"])
        resp = requests.post("http://localhost:80/taxi/datamining/buildmodel", data=json.dumps(data),headers=headers)
        print(resp)
        print(resp.text)
        resp = json.loads(resp.text)  # 获取数据
        state = resp["state"]
        if state == 13 : continue
        timeStart = resp["timeStart"]  # 当前时间
        timeStart = timeStart.split(" ")
        date = timeStart[0]
        hourAndMinute = timeStart[1]
        datas = resp["data"]  # 多个区块的信息

        buildModels(datas, hourAndMinute, date, buildModelTime)  # 训练模型

    modelBeenBuilt()
    # buildModelTime += 1
    setBuildModelTime(buildModelTime)

    # 提醒后台请求异常信息
    #requests.post("http://ip:80/")


if __name__ == "__main__":
    buildModelTime = getBuildModelTime() + 1
    print(buildModelTime)
    deleteState()
    deleteOldModel()
    deleteOldExceps()
    # geohashs = getFiveBitGeohs()
    geohashs = ["ws0ed","ws0df","ws0eh","ws0e6","ws0ed","ws0e9","ws0ef"]
    getDataToBuildModel(geohashs, buildModelTime)
