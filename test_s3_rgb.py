from machine import Pin
from time import sleep
from neopixel import NeoPixel

pin = Pin(38, Pin.OUT)  # Pin number for v1.1 of the above DevKitC
np = NeoPixel(pin, 1)  # "1" = one RGB led on the "led bus"


# 设置颜色和亮度的辅助函数
def set_color(r, g, b, brightness=0.01):
    if brightness < 0:
        brightness = 0.01
    if brightness > 1:
        brightness = 1

    r = int(r * brightness)
    g = int(g * brightness)
    b = int(b * brightness)
    np[0] = (r, g, b)
    np.write()


while True:
    set_color(255, 0, 0)  # 红色
    sleep(1)
    set_color(0, 255, 0)  # 绿色
    sleep(1)
    set_color(0, 0, 255)  # 蓝色
    sleep(1)
    set_color(255, 255, 0)  # 黄色
    sleep(1)
    set_color(0, 255, 255)  # 青色
    sleep(1)
    set_color(255, 0, 255)  # 洋红
    sleep(1)
    set_color(255, 255, 255)  # 白色
    sleep(1)
