from machine import I2S, Pin
import time
import array
import math

# I2S 配置
# MAX98357A 引脚连接:
# BCLK -> GPIO16
# LRC(WS) -> GPIO17
# DIN -> GPIO15
# GND -> GND
# VIN -> 3.3V
# GAIN -> GND (GAIN增益)


# 初始化引脚定义
sck_pin = Pin(16)  # SCLK：串行时钟，也叫位时钟（BCLK）
ws_pin = Pin(17)  # LRCK：帧时钟，也称（WS），用于切换左右声道的数据。
sd_pin = Pin(15)  # 串行数据输出

# 参数配置
sample_rate = 16000  # 采样率
bits_per_sample = 16  # 每采样位数

# 初始化I2S
audio_out = None


def init_player():
    global audio_out
    # 初始化I2S
    audio_out = I2S(
        1,
        sck=sck_pin,
        ws=ws_pin,
        sd=sd_pin,
        mode=I2S.TX,
        bits=bits_per_sample,
        format=I2S.MONO,
        rate=sample_rate,
        ibuf=20000
    )
    print('Audio out I2S init.')


def play_audio(buf: bytes):
    if audio_out:
        audio_out.write(buf)


def start_out(buf: bytes):
    if not buf:
        return

    block_size = 2048
    audio_data = bytearray(buf)
    # wav_samples_mv = memoryview(wav_samples)

    print("start out ...")

    # 分块播放音频数据
    for i in range(0, len(audio_data), block_size):
        # 获取当前块的数据
        chunk = audio_data[i:i + block_size]

        # 播放当前块的音频数据
        audio_out.write(chunk)  # 使用 I2S 播放数据块

        # 暂停一会儿，确保音频播放完成（如果需要的话）
        # time.sleep(0.1)  # 根据需要调整时间
    print(' out end')


# 播放固定大小的数据块
def play_chunks(chunk_size):
    """
    从缓冲区中读取固定大小的数据块，并播放。

    :param chunk_size: 每次播放的字节数。
    """
    global buffer
    while len(buffer) >= chunk_size:
        chunk = buffer[:chunk_size]  # 取出前 chunk_size 字节
        buffer = buffer[chunk_size:]  # 从缓冲区中移除已播放的数据
        # 模拟播放数据
        print(f"播放: {chunk} (大小: {len(chunk)} 字节)")


def deinit_player():
    if audio_out:
        audio_out.deinit()
        print('Audio out I2S deinit.')
