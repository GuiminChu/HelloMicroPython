def cmd_thx():
    """ 谢谢 """

    cmd = 0x0F
    feedback = 0x01
    dat = [0x03, 0x02]
    return send_cmd(cmd, feedback, dat)


def cmd_need_water():
    """ 需要浇水 """
    cmd = 0x0F
    feedback = 0x01
    dat = [0x03, 0x01]
    return send_cmd(cmd, feedback, dat)


def cmd_no_need_water():
    """ 不需要浇水 """

    cmd = 0x0F
    feedback = 0x01
    dat = [0x03, 0x03]
    return send_cmd(cmd, feedback, dat)


def send_cmd(cmd, feedback, dat):
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


def calculate_checksum(bytes_data: list):
    checksum = sum(bytes_data)
    checksum = ~checksum & 0xFFFF
    checksum += 1

    checksum_high = checksum >> 8
    checksum_low = checksum & 0xFF

    return checksum_high, checksum_low
