def changeDate(year, month, day, hour, minute, timeBlock=6):
    """ 时间变幻 """
    if minute < timeBlock:  # 更新时间
        minute = 60 - timeBlock
        if hour == 0:           # 跳转到上一个小时
            hour = 23
            if day == 1:        # 跳转到上一天
                day = 30
                if month == 1:      # 跳转到上一个月，年份跳转
                    month = 12
                    year -= 1
                else :          # 只跳转月份，年份没变
                    month -= 1
            else:
                day -= 1        # 只跳转天数，月份没变
        else:
            hour -= 1           # 只跳转小时，不跳转天数
    else:           # 只跳转分钟，不跳转小时
        minute -= timeBlock
    return year, month, day, hour, minute


def dateToTime(year, month, day, hour, minute):
    """ 将时间整合，转化为完整的时间格式 """
    if minute < 10:
        minute = "0" + str(minute)
    if hour < 10:
        hour = "0" + str(hour)
    if day < 10:
        day = "0" + str(day)
    if month < 10:
        month = "0" + str(month)
    time = str(year) + "-" + str(month) + "-" +str(day) + " " + str(hour) + ":" + str(minute) + ":00"
    return time