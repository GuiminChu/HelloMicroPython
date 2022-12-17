from machine import Pin
import time


class LED:
    pin2 = Pin(2, Pin.OUT)
    pin4 = Pin(4, Pin.OUT)

    def __init__(self, pin: int):
        self.pin = Pin(pin, Pin.OUT)

    def on(self):
        self.pin.on()

    def off(self):
        self.pin.off()

    @classmethod
    def pin2_on(cls):
        cls.pin2.on()

    @classmethod
    def pin2_off(cls):
        cls.pin2.off()

    @classmethod
    def pin2_blink_on(cls):
        for i in range(0, 3):
            cls.pin2.off()
            time.sleep(0.1)
            cls.pin2.on()
            time.sleep(0.1)

    @classmethod
    def pin2_blink_off(cls):
        for i in range(0, 3):
            cls.pin2.on()
            time.sleep(0.1)
            cls.pin2.off()
            time.sleep(0.1)

    @classmethod
    def pin4_on(cls):
        cls.pin4.on()

    @classmethod
    def pin4_off(cls):
        cls.pin4.off()
