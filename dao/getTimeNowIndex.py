def getTimeNowIndex(timeNow, timeBlock):
    """ 获取当前时间段对应的索引 """
    time = timeNow.split(":")
    hour = int(time[0])
    minute = int(time[1])
    timeIndex = (minute + hour * 60) / timeBlock + 1
    return timeIndex