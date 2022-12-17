import log
import checkNet
import request

'''
下面两个全局变量是必须有的，用户可以根据自己的实际项目修改下面两个全局变量的值
'''
PROJECT_NAME = "QuecPython_checkNet_example"
PROJECT_VERSION = "1.0.0"

checknet = checkNet.CheckNetwork(PROJECT_NAME, PROJECT_VERSION)

# 设置日志输出级别
log.basicConfig(level=log.INFO)
checknet_log = log.getLogger("CheckNet")

url = "https://icanhazip.com/"

if __name__ == '__main__':
    stagecode, subcode = checknet.wait_network_connected(30)
    if stagecode == 3 and subcode == 1:
        checknet_log.info('Network connection successful!')
        checknet.poweron_print_once()

        response = request.get(url)   # 发起http GET请求
        #checknet_log.info(response.json())  # 以json方式读取返回
        for i in response.text:  # response.text为迭代器对象
            checknet_log.info(i)

    else:
        checknet_log.info('Network connection failed! stagecode = {}, subcode = {}'.format(stagecode, subcode))
        if stagecode == 1:
            if subcode == 0:
                checknet_log.info('Please insert the SIM card.')
            else:
                checknet_log.info('The SIM card status is abnormal,Please confirm that the SIM card is available.')
        elif stagecode == 2:
            if subcode == -1:
                checknet_log.info('Get network state failed.')
            else:
                checknet_log.info('Failed to register network. ERRCODE={}'.format(subcode))
        elif stagecode == 3:
            if subcode == 0:
                checknet_log.info('Network dialing timeout.')

