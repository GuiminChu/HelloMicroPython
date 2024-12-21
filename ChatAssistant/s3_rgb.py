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


