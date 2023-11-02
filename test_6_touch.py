# ESP32 提供了多达 10 个电容式传感 GPIO，能够探测由手指或其他物品直接接触或接近而产生的电容差异。
# 电容式传感信号名称	- GPIO编号
# touch_0 - GPIO4
# touch_1   GPIO0
# touch_2   GPIO2
# touch_3   GPIO15
# touch_4   GPIO13
# touch_5   GPIO12
# touch_6   GPIO14
# touch_7   GPIO27
# touch_8   GPIO33
# touch_9   GPIO32

from machine import TouchPad, Pin
from time import sleep

blue_led = Pin(2, Pin.OUT)

# 对应模块针脚D32
touch_9 = TouchPad(Pin(32))

while True:
    touch_9_value = touch_9.read()

    print(touch_9_value)

    if touch_9_value > 500:
        blue_led.on()
    else:
        blue_led.off()

    sleep(0.5)
