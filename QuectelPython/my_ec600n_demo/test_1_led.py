from machine import Pin
from misc import PWM
import utime

def blue_led():
    user_led = Pin(Pin.GPIO15, Pin.OUT, Pin.PULL_DISABLE, 0)
    user_led.write(1)


def blink_led():
    user_led = Pin(Pin.GPIO15, Pin.OUT, Pin.PULL_DISABLE, 0)

    while True:
        user_led.write(1)
        utime.sleep(1)
        user_led.write(0)
        utime.sleep(1)

if __name__ == "__main__":
    blue_led()
    # blink_led()
