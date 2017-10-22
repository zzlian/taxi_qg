import pickle


def getFiveBitGeohs(fileName=r"E:\taxi_datamining\qg_taxi_infos\geohashs.txt"):
    """ 获取5位的geohashs """
    f = open(fileName, "rb")
    geohashs = pickle.load(f)
    return geohashs