import pickle


def excepReason(geohash, fileName=r"E:\taxi_datamining\qg_taxi_infos\excepReason.txt"):
    """ 给出异常原因分析 """
    f = open(fileName, "rb")
    reasons = pickle.load(f)
    f.close()
    n = 0
    for geoh in reasons.keys():
        m = 0
        for i in range(7):
            if geoh[i] != geohash[i]:
                break
            m += 1
        if n < m :
            n = m
            reason = reasons[geoh]
    return reason
