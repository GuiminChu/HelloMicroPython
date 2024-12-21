# 2024年12月18日
#
import time
import max98357a
import inmp441
from wifi import Wifi
import minimax_speech

max98357a.init_player()
inmp441.init_recorder()

is_connected = Wifi.do_connect()
if is_connected:
    print('wifi connected')

    while True:
        # print('程序运行中')
        if not minimax_speech.is_audio_playing:
            # 从 I2S 读取数据
            read_len = inmp441.audio_in.readinto(inmp441.read_buffer)
        # 稍作延迟，降低 CPU 占用
        time.sleep(0.1)
else:
    print('wifi not connected')
