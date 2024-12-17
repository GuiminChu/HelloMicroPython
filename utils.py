import machine


def get_current_time():
    # 获取当前时间
    rtc = machine.RTC()
    current_time = rtc.datetime()

    # 获取时分秒部分（current_time 是一个元组，格式为 (year, month, day, weekday, hour, minute, second, microsecond)）
    hour = current_time[4]
    minute = current_time[5]
    second = current_time[6]

    # 打印时分秒
    print("当前时间是：{}:{}:{}".format(hour, minute, second))
