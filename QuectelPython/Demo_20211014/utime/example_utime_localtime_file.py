'''
@Author: Baron
@Date: 2020-06-17
@LastEditTime: 2020-06-17 17:06:08
@Description: example for module utime
@FilePath: example_utime_loacltime_file.py
'''
import utime
import log


'''
下面两个全局变量是必须有的，用户可以根据自己的实际项目修改下面两个全局变量的值
'''
PROJECT_NAME = "QuecPython_localtime_example"
PROJECT_VERSION = "1.0.0"


# 设置日志输出级别
log.basicConfig(level=log.INFO)
time_log = log.getLogger("LocalTime")

if __name__ == '__main__':
    # 获取本地时间，返回元组
    tupe_t = utime.localtime()
    time_log.info(tupe_t)