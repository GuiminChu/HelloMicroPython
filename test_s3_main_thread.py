# 2024年12月18日
#
from machine import Pin
from wifi import Wifi

import time
import max98357a
import inmp441
import minimax_speech
import utils
import _thread

mqtt_client = None

is_connected = False

is_listening = True
is_audio_playing = False
# is_audio_receiving = False
audio_buffer = bytearray()
audio_chunk_size = 2048
read_index = 0  # 读取指针

motion = False

max98357a.init_player()
inmp441.init_recorder()


def get_tts():
    utils.get_current_time()
    minimax_speech.tts_mrequest("你好吗？")


def handle_interrupt(pin):
    global motion
    if not motion:
        print("触发")
        motion = True
        utils.get_current_time()
        _thread.start_new_thread(get_tts, ())


pir = Pin(11, Pin.IN)
pir.irq(trigger=Pin.IRQ_RISING, handler=handle_interrupt)

is_connected = Wifi.do_connect()
if is_connected:
    print('wifi connected')

    while True:
        # print('程序运行中')
        # 从 I2S 读取数据
        read_len = inmp441.audio_in.readinto(inmp441.read_buffer)
        # 稍作延迟，降低 CPU 占用
        time.sleep(0.1)
else:
    print('wifi not connected')
