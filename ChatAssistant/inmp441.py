from machine import I2S, Pin
#from ulab import numpy as np
import numpy as np
import time
import utils
import minimax_speech
from ChatAssistant import ali_speech_recognizer
import _thread

audio_in = None


def init_recorder():
    global audio_in

    # 初始化引脚定义
    ws_pin = Pin(4)  # LRCK：帧时钟，也称（WS），用于切换左右声道的数据。
    sck_pin = Pin(5)  # SCLK：串行时钟，也叫位时钟（BCLK）
    sd_pin = Pin(6)  # 串行数据输出

    # 初始化I2S
    audio_in = I2S(
        0,
        sck=sck_pin,
        ws=ws_pin,
        sd=sd_pin,
        mode=I2S.RX,
        bits=bits_per_sample,
        format=I2S.MONO,
        rate=sample_rate,
        ibuf=20000  # 缓冲区大小
    )
    print('Audio in I2S init.')

    # 注册事件与回调
    audio_in.irq(i2s_callback)


# 参数配置
sample_rate = 16000  # 采样率
bits_per_sample = 16  # 每采样位数
num_channels = 1  # 单声道
frame_duration = 0.1  # 每帧时长（秒）
frame_samples = int(sample_rate * frame_duration)  # 每帧采样数
bytes_per_sample = bits_per_sample // 8
read_buffer = bytearray(frame_samples * bytes_per_sample)
recorded_data = bytearray()

silence_threshold = 1500  # 静音阈值，样本绝对值低于此值认为是静音
silence_duration = 1.0  # 静音持续时间（秒）

recording = False  # 是否在录音

last_active_time = time.ticks_ms()


# 事件回调函数
def i2s_callback(i2s):
    global recording, last_active_time

    # 计算当前帧是否为静音
    audio_data = np.frombuffer(read_buffer, dtype=np.int16)
    temp = np.max(audio_data)
    # print(temp)
    if temp > silence_threshold:
        if not recording:
            print(f"检测到声音，开始录音... 时间: {utils.get_current_time()}")
            recording = True

        last_active_time = time.ticks_ms()
        # print(f"last_active_time: {last_active_time}")

    if recording:
        recorded_data.extend(read_buffer)

        if time.ticks_diff(time.ticks_ms(), last_active_time) > silence_duration * 1000:
            print(f"检测到静音，录音结束。时间: {utils.get_current_time()}")
            recording = False
            minimax_speech.is_audio_playing = True
            _thread.start_new_thread(get_tts, ())


def get_tts():
    global recorded_data
    text = ali_speech_recognizer.speech_recognizer(recorded_data)
    recorded_data = bytearray()
    print(f"获取录音识别结果: [{text}]，开始请求语音，时间: {utils.get_current_time()}")
    if text:
        minimax_speech.tts_mrequest(text)
    else:
        minimax_speech.is_audio_playing = False
        print("识别结果为空，结束执行。")