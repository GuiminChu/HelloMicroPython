'''
@Author: Baron
@Date: 2020-04-24
@LastEditTime: 2020-04-24 17:06:08
@Description: example for module umqtt
@FilePath: example_mqtt_file.py
'''
from umqtt import MQTTClient
import utime
import log
import checkNet

'''
下面两个全局变量是必须有的，用户可以根据自己的实际项目修改下面两个全局变量的值
'''
PROJECT_NAME = "QuecPython_MQTT_example"
PROJECT_VERSION = "1.0.0"

# MQTT_SERVER = b'192.168.1.101'
# MQTT_PORT = 1883
MQTT_SERVER = b'223.99.228.240'
MQTT_PORT = 11883
MQTT_CLIENT_ID = b'4435293940613'  # 客户端的ID
MQTT_USERNAME = b'kAZDgUfD'
MQTT_PASSWORD = b'1562723342481948673'

MQTT_TOPIC_TEST = b'ec600n/test/4435293940613'
MQTT_TOPIC_DHT = b'esp32/dht22/3571116'
MQTT_TOPIC_LED = b'esp32/led/3571116'

checknet = checkNet.CheckNetwork(PROJECT_NAME, PROJECT_VERSION)

# 设置日志输出级别
log.basicConfig(level=log.INFO)
mqtt_log = log.getLogger("MQTT")

mqtt_client = None
state = 0


def sub_cb(topic, msg):
    global state
    mqtt_log.info("Subscribe Recv: Topic={},Msg={}".format(topic.decode(), msg.decode()))
    state = 1


def mqtt_init():
    # 创建一个mqtt实例
    c = MQTTClient(MQTT_CLIENT_ID, MQTT_SERVER, MQTT_PORT, MQTT_USERNAME, MQTT_PASSWORD, 30)
    # 设置消息回调
    c.set_callback(sub_cb)
    # 建立连接
    c.connect()
    # 订阅主题
    c.subscribe(MQTT_TOPIC_DHT)
    mqtt_log.info("Connected to server, subscribed to /public/TEST/quecpython topic")

    # 发布消息
    c.publish(MQTT_TOPIC_TEST, b"my name is QuecPython!")
    mqtt_log.info("Publish topic: /public/TEST/quecpython, msg: my name is Quecpython")

    while True:
        c.wait_msg()
        if state == 1:
            break

    # 关闭连接
    c.disconnect()


if __name__ == '__main__':
    stagecode, subcode = checknet.wait_network_connected(30)
    if stagecode == 3 and subcode == 1:
        mqtt_log.info('Network connection successful!')

        mqtt_init()

    else:
        mqtt_log.info('Network connection failed! stagecode = {}, subcode = {}'.format(stagecode, subcode))
