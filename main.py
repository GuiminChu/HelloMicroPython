from wifi import Wifi
from led import LED
from umqtt_simple import MQTTClient
from machine import Pin
from machine import Timer
import machine
import dht
import json
import time
import ubinascii

MQTT_SERVER = '223.99.228.240'
MQTT_PORT = 11883
# MQTT_SERVER = '192.168.1.101'
# MQTT_PORT = 1883
# MQTT_CLIENT_ID = '3571116'  # 客户端的ID
MQTT_CLIENT_ID = ubinascii.hexlify(machine.unique_id())

MQTT_USERNAME = 'kAZDgUfD'
MQTT_PASSWORD = '1562723342481948673'

MQTT_TOPIC_LAST_WILL = b'esp32/will/3571116'

MQTT_TOPIC_DHT = b'esp32/dht22/3571116'
MQTT_TOPIC_LED = b'esp32/led/3571116'

mqtt_client = None

is_connected = False


def heartbeat_timer(my_timer: Timer):
    try:
        dht22.measure()
        print(dht22.temperature())
        print(dht22.humidity())

        d1 = {
            "deviceSn": MQTT_CLIENT_ID,
            "temperature": dht22.temperature(),
            "humidity": dht22.humidity()
        }

        j1 = json.dumps(d1)
        print(j1)
        mqtt_client.publish(MQTT_TOPIC_DHT, j1)
        LED.pin2_blink_on()
    except OSError as e:
        print(e)
        my_timer.deinit()


def sub_cb(topic, msg):
    print('Received Message %s from topic %s' % (msg, topic))

    msg = json.loads(msg)
    if msg['ledStatus'] == 'ON':
        LED.pin4_on()
        print('Led on')
    if msg['ledStatus'] == "OFF":
        LED.pin4_off()
        print('Led off')


is_connected = Wifi.do_connect()
if is_connected:
    LED.pin2_on()

    mqtt_client = MQTTClient(MQTT_CLIENT_ID, MQTT_SERVER, MQTT_PORT, MQTT_USERNAME, MQTT_PASSWORD, 30)
    mqtt_client.connect()
    mqtt_client.set_callback(sub_cb)
    mqtt_client.subscribe(MQTT_TOPIC_LED)

    dht22 = dht.DHT22(Pin(15))

    timer0 = Timer(0)
    timer0.init(period=10000, mode=Timer.PERIODIC, callback=heartbeat_timer)

    while True:
        try:
            mqtt_client.check_msg()
        except OSError as e:
            print(e)
else:
    print('wifi not connected')
