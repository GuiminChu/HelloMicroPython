# 2024年12月18日
#
from machine import UART, Timer, Pin
import time
import max98357a
import inmp441
import oled_091
from wifi import Wifi
import minimax_speech
import ali_speech_recognizer
import utils

max98357a.init_player()
inmp441.init_recorder()
oled_091.init()
oled_091.show("Hello, world!")

# 设置波特率115200
uart1 = UART(1, 115200, rx=Pin(18))

# 创建一个Timer，使用timer的中断来轮询串口是否有可读数据
timer = Timer(1)
timer.init(period=50, mode=Timer.PERIODIC, callback=lambda t: read_uart(uart1))


def read_uart(uart):
    if uart.any():
        # 将接收到的16进制数据转换为字符串
        ur = uart.read().hex()
        print(f"uart1 received: {ur}, time: {utils.get_current_time()}")
        if ur == '0a0a':
            minimax_speech.get_tts("我在")
            inmp441.is_wake_up = True
        elif ur == '0e0d':
            pass


is_connected = Wifi.do_connect()
if is_connected:
    print('wifi connected')
    ali_speech_recognizer.get_token()

    while True:
        # print('程序运行中')
        if not minimax_speech.is_audio_playing and inmp441.is_wake_up:
            # 从 I2S 读取数据
            inmp441.record_audio()
            oled_091.show("Listening...")
        if minimax_speech.is_audio_playing:
            oled_091.show("Speaking...")
        # 稍作延迟，降低 CPU 占用
        time.sleep(0.1)
else:
    print('wifi not connected')
