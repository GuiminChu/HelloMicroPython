from machine import Pin, I2C
import ssd1306

display = None


def init():
    global display

    i2c = I2C(-1, scl=Pin(10), sda=Pin(11))
    display = ssd1306.SSD1306_I2C(128, 32, i2c)


def show(text):
    display.text(text, 0, 0, 1)
    display.show()
