from machine import UART
from machine import Timer
import time

# 默认波特率115200
uart2 = UART(2)

# 创建一个Timer，使用timer的中断来轮询串口是否有可读数据
timer = Timer(1)
timer.init(period=50, mode=Timer.PERIODIC, callback=lambda t: read_uart(uart2))


def read_uart(uart):
    if uart.any():
        print('received: ' + uart.read().decode() + '\n')


if __name__ == '__main__':
    try:
        for i in range(10):
            # uart2.write(input('send: '))
            uart2.write('hello esp32')
            time.sleep_ms(1000)
    except:
        timer.deinit()
