from machine import I2S, Pin
# from ulab import numpy as np
import time
import struct
import numpy as np
from test_speech_recognizer import speech_recognizer
from wifi import Wifi

Wifi.do_connect()


# WAV 文件头生成函数
def generate_wav_header(sample_rate, bits_per_sample, num_channels, data_size):
    byte_rate = sample_rate * num_channels * (bits_per_sample // 8)
    block_align = num_channels * (bits_per_sample // 8)

    return (b'RIFF' +
            struct.pack('<I', 36 + data_size) +
            b'WAVEfmt ' +
            struct.pack('<IHHIIHH', 16, 1, num_channels, sample_rate, byte_rate, block_align, bits_per_sample) +
            b'data' +
            struct.pack('<I', data_size))


# 初始化引脚定义
ws_pin = Pin(4)  # LRCK：帧时钟，也称（WS），用于切换左右声道的数据。
sck_pin = Pin(5)  # SCLK：串行时钟，也叫位时钟（BCLK）
sd_pin = Pin(6)  # 串行数据输出

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
silence_duration = 1.2  # 静音持续时间（秒）

recording = False  # 是否在录音

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

print("等待音频输入...")
last_active_time = time.ticks_ms()

while True:
    try:
        # 从 I2S 读取数据
        read_len = audio_in.readinto(read_buffer)
        if read_len:
            # 计算当前帧是否为静音
            audio_data = np.frombuffer(read_buffer, dtype=np.int16)
            temp = np.max(audio_data)
            print(temp)
            if temp > silence_threshold:
                if not recording:
                    print("检测到声音，开始录音...")
                    recording = True

                last_active_time = time.ticks_ms()
                print(f"last_active_time: {last_active_time}")

            if recording:
                recorded_data.extend(read_buffer[:read_len])

                if time.ticks_diff(time.ticks_ms(), last_active_time) > silence_duration * 1000:
                    print("检测到静音，录音结束。")
                    recording = False
                    print(f"current_time: {time.ticks_ms()}")
                    break

        # 稍作延迟，降低 CPU 占用
        time.sleep(0.1)

    except Exception as e:
        print("读取错误:", e)
        break

# 保存录音为 WAV 文件
if recorded_data:
    speech_recognizer(recorded_data)

else:
    print("未检测到有效音频，未保存文件。")
