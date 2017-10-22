def changeToOneHot(timeNow, timeBlock=6):
    """ 计算当前时间对应的one-hot编码 """
    time = timeNow.split(":")
    hour = int(time[0])  # 当前小时
    minute = int(time[1])  # 当前分钟
    oneHotBlocks = (6 * 60) / 6  # 编码对应的时间间隔数
    if hour > 23 or hour <= 5:
        oneHotIndex = 0  # 该时段的one-hot编号
        if hour > 23:
            timeIndex = int(minute / timeBlock)  # 对应与该编码区段的小时段
        else:
            timeIndex = 60 / 6 + int((hour * 60 + minute) / 6)
    elif hour <= 11:
        oneHotIndex = 1
        timeIndex = int(((hour - 5) * 60 + minute) / 6)
    elif hour <= 17:
        oneHotIndex = 2
        timeIndex = int(((hour - 11) * 60 + minute) / 6)
    else:
        oneHotIndex = 3
        timeIndex = int(((hour - 17) * 60 + minute) / 6)
    timeIndex += 1
    if timeIndex > oneHotBlocks:
        timeIndex = 1
        if oneHotIndex == 3: oneHotIndex = 0
        else: oneHotIndex += 1
    return oneHotIndex, timeIndex