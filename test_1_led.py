from machine import Pin, PWM
import time


def blue_led():
    pin2 = Pin(2, Pin.OUT)
    # pin2.value(0)
    pin2.on()
    print(pin2.value())


def blink_led():
    pin2 = Pin(2, Pin.OUT)

    while True:
        pin2.on()
        time.sleep(1)
        pin2.off()
        time.sleep(1)


def breath_led():
    led2 = PWM(Pin(2))
    led2.freq(1000)

    while True:
        for i in range(0, 1024):
            led2.duty(i)
            time.sleep_ms(1)

        for i in range(1023, -1, -1):
            led2.duty(i)
            time.sleep_ms(1)


if __name__ == "__main__":
    # blue_led()
    # blink_led()
    breath_led()
