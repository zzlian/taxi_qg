from dao.handleModels import getModels


def isError(data):
    """ 判断后台给的数据是否有误 """
    flag = 0
    for value in data.values():
        if len(value) < 3:      #列表数据小于3个则不正常
            print("数据信息有误，不满3个:",value)
            flag = 1
            break
    if flag == 0 :
        models = getModels()
        geohs = models.keys()
        predictGeohs = list(data.keys())[:]
        for key in set(predictGeohs):  # 删除掉不存在的geohash
            if key not in geohs:
                print(key, "不存在，该区域无法预测！！")
                del data[key]
        if not data:
            print("所有请求的geohash都不存在：",predictGeohs)
            print("可预测的goehash：",geohs)
            flag = 1
    if flag == 1: return True   #信息有误
    else : return False     #信息正常

def isErrorInRatio(data, geoh):
    """ 判断预测车辆利用率给的数据是否异常 """
    flag = 0
    for value in data.values():
        if len(value) < 3:  # 列表数据小于3个则不正常
            print("数据信息有误，不满3个:",value)
            flag = 1
            break
    if flag == 0 :
        models = getModels()
        if geoh not in models.keys():
            print(geoh+"不存在，无法预测相应的范围")
            print("可预测的geohash：", models.keys())
            flag = 1
    if flag == 1: return True   #信息有误
    else : return False     #信息正常


def isErrorDriveTime(data, index):
    """  判断数据是否错误 """
    num = 0
    flag = 0
    for value in data.values():
        if len(value) < 3:  # 列表数据小于3个则不正常
            print("数据信息有误，不满3个:", value)
            flag = 1
            break
    if flag == 0:
        models = getModels()
        geohs = models.keys()
        predictGeohs = list(data.keys())[:]
        for key in set(predictGeohs):  # 删除掉不存在的geohash
            if key not in geohs:
                print(key, "不存在，该区域无法预测！！")
                num += 1
                index.remove(key)
                del data[key]
        if not data:
            print("所有请求的geohash都不存在：", predictGeohs)
            print("可预测的goehash：", geohs)
            flag = 1
    if flag == 1:
        return True, 0  # 信息有误
    else:
        return False, num  # 信息正常