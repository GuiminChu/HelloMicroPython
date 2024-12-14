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

wav = open("recording.wav", "rb")

# advance to first byte of Data section in WAV file
# 跳过文件的开头的44个字节，直到数据段的第1个字节
pos = wav.seek(44)

wav_samples = bytearray(2048)
wav_samples_mv = memoryview(wav_samples)

print("Test I2S.")
# 播放音频数据
# 并将其写入I2S DAC
while True:
    try:
        num_read = wav.readinto(wav_samples_mv)

        # WAV文件结束
        if num_read == 0:
            break

        # 直到所有样本都写入I2S外围设备
        num_written = 0
        while num_written < num_read:
            num_written += audio_out.write(wav_samples_mv[num_written:num_read])

    except Exception as ret:
        print("产生异常...", ret)
        break

wav.close()
audio_out.deinit()
print('Done')
