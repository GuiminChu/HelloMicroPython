from machine import Pin
from wifi import Wifi

import time
import max98357a
import minimax_speech
import utils

motion = False

max98357a.init_player()


def handle_interrupt(pin):
    global motion
    if not motion:
        print("触发")
        utils.get_current_time()
        motion = True
        audio_data = minimax_speech.tts_data("你好吗？")
        utils.get_current_time()
        max98357a.play_audio(bytes.fromhex(audio_data))
        utils.get_current_time()


pir = Pin(11, Pin.IN)
pir.irq(trigger=Pin.IRQ_RISING, handler=handle_interrupt)

is_connected = Wifi.do_connect()
if is_connected:
    print('wifi connected')

    while True:
        print('程序运行中')
        time.sleep(1)
else:
    print('wifi not connected')
