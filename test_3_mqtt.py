from umqtt_simple import MQTTClient
import time

SERVER = '223.99.228.240'
PORT = 11883
CLIENT_ID = '3571116'  # 客户端的ID

USERNAME = 'kAZDgUfD'
PASSWORD = '1562723342481948673'

TOPIC = b'pyespcar_basic_control'  # TOPIC的ID

client = MQTTClient(CLIENT_ID, SERVER, PORT, USERNAME, PASSWORD)
client.connect()

while True:
    client.publish(TOPIC, 'helloworld')
    time.sleep(1)

    client.check_msg()
