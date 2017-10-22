from utils.excepReason import excepReason


def isExceptional(time, result, y, geoh, err=20):
    """ 异常情况判断 """
    excep = {}
    if (result - y) > err or (y - result) > err:    # 异常情况处理
        print(geoh+time+"异常:", result - y)
        excep["time"] = time
        excep["geohash"] = geoh
        if (result - y) > err:  # 异常激增情况
            excep["exception"] = "数量激增"
            reason = excepReason(geoh)  # 异常原因分析
            excep["reason"] = reason
        elif (y - result) > err:
            excep["exception"] = "数量骤减"
            excep["reason"] = "过节人流减少"  # 异常情况分析
        return True, excep
    else : return False, []     # 无异常