from machine import Pin, SPI, ADC, UART, Timer
import ssd1306
import dht
from wifi import Wifi
from umqtt_simple import MQTTClient
import json
from led import LED
from ldr import LDR
import yx5300

MQTT_SERVER = '223.99.228.240'
MQTT_PORT = 11883
MQTT_CLIENT_ID = 'c8f09e9f885c'
MQTT_USERNAME = 'YGIWipTdbim'
MQTT_PASSWORD = '1721713448384507906'

MQTT_TOPIC_SYS_REPORT = f'$SYS/{MQTT_USERNAME}/{MQTT_CLIENT_ID}/thing/properties/report'
MQTT_TOPIC_SYS_SET = f'$SYS/{MQTT_USERNAME}/{MQTT_CLIENT_ID}/thing/properties/set'
MQTT_TOPIC_SYS_COMMAND = f'$SYS/{MQTT_USERNAME}/{MQTT_CLIENT_ID}/thing/commands'

SOIL_DRY = 540
SOIL_WET = 340

soil_moisture = 0

# initialize an LDR
ldr = LDR(35)

# 是否是夜晚
is_night = False

vspi = SPI(2, baudrate=80000000, polarity=0, phase=0, bits=8, firstbit=0, sck=Pin(18), mosi=Pin(23), miso=Pin(19))
dc = Pin(22)  # data/command
rst = Pin(21)  # reset
cs = Pin(13)  # chip select, some modules do not have a pin for this

display = ssd1306.SSD1306_SPI(128, 64, vspi, dc, rst, cs)

# 土壤湿度传感器
soil_moisture_sensor = ADC(Pin(34))
soil_moisture_sensor.atten(ADC.ATTN_11DB)  # 这里配置测量量程为3.3V
soil_moisture_sensor.width(ADC.WIDTH_10BIT)

# 继电器高电平触发引脚
water_relay = Pin(12, Pin.OUT)
# 浇水指示灯
water_led = Pin(4, Pin.OUT)

# 声明一个 UART 对象，使用 UART2，波特率 9600
uart2 = UART(2, baudrate=9600)

# 创建一个 Timer，使用 timer 的中断来轮询串口是否有可读数据
timer1 = Timer(1)
timer1.init(period=50, mode=Timer.PERIODIC, callback=lambda t: read_uart(uart2))


def read_uart(uart):
    if uart.any():
        # 将接收到的16进制数据转换为字符串
        print('received: ' + uart.read().hex() + '\n')


def mqtt_heartbeat_timer(my_timer: Timer):
    global soil_moisture
    global is_night

    try:
        # 测量土壤湿度
        soil_moisture = soil_moisture_sensor.read()
        # 测量光照强度
        ldr_value = ldr.value()
        # 测量温湿度
        dht22.measure()

        if ldr_value < 17:
            is_night = True
        else:
            is_night = False

        d1 = {
            "services": [
                {
                    "serviceId": "DEFAULT",
                    "properties": {
                        "soil_moisture": soil_moisture,
                        "light_intensity": ldr_value,
                        "temperature": dht22.temperature(),
                        "humidity": dht22.humidity(),
                        # "onoff_states": is_led_open
                    }
                }
            ]
        }

        j1 = json.dumps(d1)
        print(j1)
        mqtt_client.publish(MQTT_TOPIC_SYS_REPORT, j1)
        LED.pin2_blink_on()
    except OSError as e:
        print(e)
        my_timer.deinit()


# mqtt 消息回调函数
def mqtt_sub_cb(topic, msg):
    print('Received Message %s from topic %s' % (msg, topic))
    print(type(topic))
    # 将topic 转为 str
    topic = str(topic, 'utf-8')

    if topic == MQTT_TOPIC_SYS_SET or topic == MQTT_TOPIC_SYS_COMMAND:
        # 解析 JSON 数据
        json_data = json.loads(msg)

        # 获取 "services" 数组
        services = json_data['services']

        # 遍历并解析每个服务
        for service in services:
            # 获取 "serviceId" 的值
            service_id = service.get('serviceId')
            # 打印解析结果
            print("Service ID:", service_id)

            # 获取 "properties" 的值
            if properties := service.get('properties'):
                # 获取 "onoff_states" 和 "text" 的值
                onoff_states: int = properties['onoff_states']

                # 打印解析结果
                print("Service ID:", service_id)
                print("On/Off States:", onoff_states)

                if onoff_states == "0":
                    LED.pin4_off()
                    is_led_open = False
                    print('Led off')

                if onoff_states == "1":
                    LED.pin4_on()
                    is_led_open = True
                    print('Led on')

            if commands := service.get('commands'):
                print(commands)

                # 浇水指令
                if water_on := commands.get('water_on'):
                    print(water_on)
                    if water_on == "1":
                        print(f'soil_moisture: {soil_moisture}')
                        # 目前土壤湿度较大
                        if soil_moisture < SOIL_WET:
                            print('no need water')
                            # 播放语音 - 不需要浇水
                            uart_cmd = yx5300.cmd_no_need_water()
                            print(uart_cmd)
                            uart2.write(bytes(uart_cmd))
                        else:
                            print('need water')
                            # 浇水
                            water_relay.on()
                            water_led.on()

                            # 播放语音 - 谢谢
                            uart_cmd = yx5300.cmd_thx()
                            print(f'uart_cmd: {uart_cmd}')
                            print(uart2)
                            uart2.write(bytes(uart_cmd))

                    else:
                        water_relay.off()
                        water_led.off()
                        print('water off')

                # 浇水检测指令
                if water_check := commands.get('water_check'):
                    print(f'water_check: {water_check}')
                    if water_check == "1":
                        print(f'soil_moisture: {soil_moisture}')
                        # 目前土壤湿度较大
                        if soil_moisture < SOIL_WET:
                            print('water_check: no need water')
                            # 播放语音 - 不需要浇水
                            uart_cmd = yx5300.cmd_no_need_water()
                            print(uart_cmd)
                            uart2.write(bytes(uart_cmd))
                        else:
                            print('water_check: need water')
                            # 播放语音 - 需要浇水
                            uart_cmd = yx5300.cmd_need_water()
                            print(uart_cmd)
                            uart2.write(bytes(uart_cmd))

    else:
        msg = json.loads(msg)
        if msg['ledStatus'] == 'ON':
            LED.pin4_on()
            print('Led on')
        if msg['ledStatus'] == "OFF":
            LED.pin4_off()
            print('Led off')


# 连接 wifi
is_wifi_connected = Wifi.do_connect()
if is_wifi_connected:
    LED.pin2_on()

    mqtt_client = MQTTClient(MQTT_CLIENT_ID, MQTT_SERVER, MQTT_PORT, MQTT_USERNAME, MQTT_PASSWORD, 30)
    mqtt_client.connect()
    mqtt_client.set_callback(mqtt_sub_cb)
    # mqtt_client.subscribe(MQTT_TOPIC_LED)
    mqtt_client.subscribe(MQTT_TOPIC_SYS_SET)
    mqtt_client.subscribe(MQTT_TOPIC_SYS_COMMAND)

    dht22 = dht.DHT22(Pin(26))

    timer0 = Timer(0)
    timer0.init(period=3000, mode=Timer.PERIODIC, callback=mqtt_heartbeat_timer)

    while True:
        try:
            mqtt_client.check_msg()
        except OSError as e:
            print(e)
else:
    print('wifi not connected')
