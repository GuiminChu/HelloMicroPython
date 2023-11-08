from machine import Pin, TouchPad, UART, Timer
from time import sleep

blue_led = Pin(2, Pin.OUT)

touch_9 = TouchPad(Pin(32))

uart2 = UART(2, baudrate=9600)

# 创建一个Timer，使用timer的中断来轮询串口是否有可读数据
timer = Timer(1)
timer.init(period=50, mode=Timer.PERIODIC, callback=lambda t: read_uart(uart2))


def read_uart(uart):
    if uart.any():
        # print('received: ' + uart.read().decode() + '\n')
        print('received: ' + uart.read().hex() + '\n')


def calculate_checksum(bytes_data: list):
    checksum = sum(bytes_data)
    checksum = ~checksum & 0xFFFF
    checksum += 1

    checksum_high = checksum >> 8
    checksum_low = checksum & 0xFF

    # bytes_data.append(checksum_high)
    # bytes_data.append(checksum_low)
    return checksum_high, checksum_low


def uart_send_cmd(cmd, feedback, dat):
    # 版本号、长度、cmd、是否反馈、数据
    send_buf = [0xFF, 0x06, cmd, feedback]
    send_buf.extend(dat)
    # print(send_buf)
    checksum_high, checksum_low = calculate_checksum(send_buf)
    send_buf.append(checksum_high)
    send_buf.append(checksum_low)
    send_buf.insert(0, 0x7E)
    send_buf.append(0xEF)
    return send_buf


while True:
    touch_9_value = touch_9.read()

    print(touch_9_value)

    if touch_9_value > 500:
        blue_led.on()
    else:
        blue_led.off()

        cmd = 0x48
        feedback = 0x00
        dat = [0x00, 0x00]
        x = uart_send_cmd(cmd, feedback, dat)
        print(x)
        print(bytes(x))

        # y = [0x7E, 0xFF, 0x06, 0x48, 0x00, 0x00, 0x00, 0xFE, 0xB3, 0xEF]
        uart2.write(bytes(x))
        # uart2.write(bytes(y))

    sleep(0.5)

# while True:
#     uart2.write(bytes.fromhex('7EFF063F000000FEBCEF'))
#     if uart2.any():
#         print('received: ' + uart2.read().hex() + '\n')
#         uart2.write(bytes.fromhex('7EFF063F000000FEBCEF'))
