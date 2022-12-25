from machine import Pin, SPI
import ssd1306

# hspi = SPI(1)  # sck=14 (scl), mosi=13 (sda), miso=12 (unused)

dc = Pin(22)  # data/command
rst = Pin(21)  # reset
cs = Pin(13)  # chip select, some modules do not have a pin for this
vspi = SPI(2, baudrate=80000000, polarity=0, phase=0, bits=8, firstbit=0, sck=Pin(18), mosi=Pin(23), miso=Pin(19))

display = ssd1306.SSD1306_SPI(128, 64, vspi, dc, rst, cs)
display.text('Hello, World!!!', 0, 0, 1)
display.text('Hello, World!!!', 0, 10, 1)
display.show()
