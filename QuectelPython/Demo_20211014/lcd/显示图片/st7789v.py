# -*- coding: UTF-8 -*-

import log
from machine import LCD


XSTART_H = 0xf0
XSTART_L = 0xf1
YSTART_H = 0xf2
YSTART_L = 0xf3
XEND_H = 0xE0
XEND_L = 0xE1
YEND_H = 0xE2
YEND_L = 0xE3


XSTART = 0xD0
XEND = 0xD1
YSTART = 0xD2
YEND = 0xD3


class ST7789V():
    def __init__(self, width, hight):
        self.lcdlog = log.basicConfig()
        self.lcdlog = log.getLogger("LCD")
        self.lcdlog.setLevel(log.DEBUG)
        self.lcd = LCD()
        self.lcd_w = width
        self.lcd_h = hight

        self.st7789v_init_data = (
            2, 1, 120,
            0, 0, 0x11,
            2, 1, 120,
            0, 1, 0x36,
            1, 1, 0x00,
            0, 1, 0x3A,
            1, 1, 0x05,
            0, 0, 0x21,
            0, 5, 0xB2,
            1, 1, 0x05,
            1, 1, 0x05,
            1, 1, 0x00,
            1, 1, 0x33,
            1, 1, 0x33,
            0, 1, 0xB7,
            1, 1, 0x23,
            0, 1, 0xBB,
            1, 1, 0x22,
            0, 1, 0xC0,
            1, 1, 0x2C,
            0, 1, 0xC2,
            1, 1, 0x01,
            0, 1, 0xC3,
            1, 1, 0x13,
            0, 1, 0xC4,
            1, 1, 0x20,
            0, 1, 0xC6,
            1, 1, 0x0F,
            0, 2, 0xD0,
            1, 1, 0xA4,
            1, 1, 0xA1,
            0, 1, 0xD6,
            1, 1, 0xA1,
            0, 14, 0xE0,
            1, 1, 0x70,
            1, 1, 0x06,
            1, 1, 0x0C,
            1, 1, 0x08,
            1, 1, 0x09,
            1, 1, 0x27,
            1, 1, 0x2E,
            1, 1, 0x34,
            1, 1, 0x46,
            1, 1, 0x37,
            1, 1, 0x13,
            1, 1, 0x13,
            1, 1, 0x25,
            1, 1, 0x2A,
            0, 14, 0xE1,
            1, 1, 0x70,
            1, 1, 0x04,
            1, 1, 0x08,
            1, 1, 0x09,
            1, 1, 0x07,
            1, 1, 0x03,
            1, 1, 0x2C,
            1, 1, 0x42,
            1, 1, 0x42,
            1, 1, 0x38,
            1, 1, 0x14,
            1, 1, 0x14,
            1, 1, 0x27,
            1, 1, 0x2C,
            0, 0, 0x29,

            0, 1, 0x36,
            1, 1, 0x00,

            0, 4, 0x2a,
            1, 1, 0x00,
            1, 1, 0x00,
            1, 1, 0x00,
            1, 1, 0xef,

            0, 4, 0x2b,
            1, 1, 0x00,
            1, 1, 0x00,
            1, 1, 0x00,
            1, 1, 0xef,

            0, 0, 0x2c,
        )

        self.st7789v_invalid_data = (
            0,4,0x2a,
            1,1,XSTART_H,
            1,1,XSTART_L,
            1,1,XEND_H,
            1,1,XEND_L,
            0,4,0x2b,
            1,1,YSTART_H,
            1,1,YSTART_L,
            1,1,YEND_H,
            1,1,YEND_L,
            0,0,0x2c,
        )
        ret = self.lcd.lcd_init(bytearray(self.st7789v_init_data), self.lcd_w, self.lcd_h, 13000, 1, 4, 0, bytearray(self.st7789v_invalid_data), None, None, None)
        self.lcdlog.info('lcd.lcd_init ret = {}'.format(ret))
        '''?????????????????????'''
        self.lcd.lcd_clear(0xFFFF)

    '''
    ????????????????????????????????????ASCII
    x - x?????????
    y - y?????????
    xsize - ????????????
    ysize - ????????????
    ch_buf - ???????????????????????????????????????
    fc - ???????????????RGB565
    bc - ???????????????RGB565
    '''
    def lcd_show_char(self, x, y, xsize, ysize, ch_buf, fc, bc):
        rgb_buf = []
        t1 = xsize // 8
        t2 = xsize % 8
        if t2 != 0:
            xsize = (t1 + 1) * 8
        for i in range(0, len(ch_buf)):
            for j in range(0, 8):
                if (ch_buf[i] << j) & 0x80 == 0x00:
                    rgb_buf.append(bc & 0xff)
                    rgb_buf.append(bc >> 8)
                else:
                    rgb_buf.append(fc & 0xff)
                    rgb_buf.append(fc >> 8)
        self.lcd.lcd_write(bytearray(rgb_buf), x, y, x + xsize - 1, y + ysize - 1)

    '''
    ASCII????????????,????????????8x16???16x24??????????????????
    ?????????????????????????????????????????????????????????????????????????????????
    ??????????????????????????????????????????????????????
    x - x???????????????
    y - y???????????????
    xsize - ????????????
    ysize - ????????????
    ch - ????????????ASCII??????
    fc - ???????????????RGB565
    bc - ???????????????RGB565
    '''
    def lcd_show_ascii(self, x, y, xsize, ysize, ch, fc, bc):
        ascii_dict = {}
        if xsize == 8 and ysize == 16:
            ascii_dict = fonts.ascii_8x16_dict
        elif xsize == 16 and ysize == 24:
            ascii_dict = fonts.ascii_16x24_dict

        for key in ascii_dict:
            if ch == key:
                self.lcd_show_char(x, y, xsize, ysize, ascii_dict[key], fc, bc)

    '''
    ???????????????,????????????8x16??????????????????
    ?????????????????????????????????????????????????????????????????????????????????
    ???lcd_show_ascii?????????????????????????????????????????????
    x - x?????????
    y - y?????????
    xsize - ????????????
    ysize - ????????????
    str - ???????????? ASCII ?????????
    fc - ???????????????RGB565
    bc - ???????????????RGB565
    '''
    def lcd_show_ascii_str(self, x, y, xsize, ysize, str, fc, bc):
        xs = x
        ys = y
        if (len(str) * xsize + x) > self.lcd_w:
            raise Exception('Display out of range')
        for ch in str:
            self.lcd_show_ascii(xs, ys, xsize, ysize, ch, fc, bc)
            xs += xsize

    '''
    ????????????,????????????16x16???16x24???24x24??????????????????
    ?????????????????????????????????????????????????????????????????????????????????
    ??????????????????????????????????????????????????????
    x - x???????????????
    y - y???????????????
    xsize - ????????????
    ysize - ????????????
    ch - ????????????ASCII??????
    fc - ???????????????RGB565
    bc - ???????????????RGB565
    '''
    def lcd_show_chinese(self, x, y, xsize, ysize, ch, fc, bc):
        hanzi_dict = {}
        if xsize == 16 and ysize == 16:
            hanzi_dict = fonts.hanzi_16x16_dict
        elif xsize == 16 and ysize == 24:
            hanzi_dict = fonts.hanzi_16x24_dict
        elif xsize == 24 and ysize == 24:
            hanzi_dict = fonts.hanzi_24x24_dict

        for key in hanzi_dict:
            if ch == key:
                self.lcd_show_char(x, y, xsize, ysize, hanzi_dict[key], fc, bc)

    '''
    ?????????????????????,????????????16x16??????????????????
    ?????????????????????????????????????????????????????????????????????????????????
    ???lcd_show_chinese?????????????????????????????????????????????
    x - x?????????
    y - y?????????
    xsize - ????????????
    ysize - ????????????
    str - ????????????????????????
    fc - ???????????????RGB565
    bc - ???????????????RGB565
    '''
    def lcd_show_chinese_str(self, x, y, xsize, ysize, str, fc, bc):
        xs = x
        ys = y
        # print('chstrlen={}, w={}'.format(len(str), self.lcd_w))
        if (len(str) / 3 * xsize + x) > self.lcd_w:
            raise Exception('Display out of range')
        for i in range(0, len(str), 3):
            index = i + 3
            ch = str[i:index]
            self.lcd_show_chinese(xs, ys, xsize, ysize, ch, fc, bc)
            xs += xsize

    '''
    ????????????
    ????????????????????????80x80?????????????????????????????????????????????
    image_data - ????????????????????????RGB??????
    x - x???????????????
    y - y???????????????
    width - ????????????
    heigth - ????????????
    '''
    def lcd_show_image(self, image_data, x, y, width, heigth):
        self.lcd.lcd_write(bytearray(image_data), x, y, x + width - 1, y + heigth - 1)

    '''
    ????????????
    ????????????????????????80x80??????????????????????????????????????????????????????????????????
    ???????????????????????????????????????????????????????????????????????????????????? width * h ??????????????????????????????????????????h???????????????????????????
    h???????????????????????????????????????????????????????????? h ?????????h??????????????????????????? width * h * 2 < 4096
    path - ?????????????????????txt???????????????????????????????????? '/usr/image.txt'
    x - x???????????????
    y - y???????????????
    width - ????????????
    heigth - ????????????
    h - ??????????????????????????????
    '''
    def lcd_show_image_file(self, path, x, y, width, heigth, h):
        image_data = []
        read_n = 0  # ????????????????????????
        byte_n = 0  # ?????????
        xs = x
        ys = y
        h_step = h  # ?????????h_step????????????????????????
        h1 = heigth // h_step  # ???????????????h_step????????????????????????????????? width * h_step ???????????????
        h2 = heigth % h_step  # ????????????????????? ???????????? width * h_step ????????????????????????
        # print('h1 = {}, h2 = {}'.format(h1, h2))
        with open(path, "r", encoding='utf-8') as fd:
            # for line in fd.readlines():
            end = ''
            while not end:
                line = fd.readline()
                if line == '':
                    end = 1
                else:
                    curline = line.strip('\r\n').strip(',').split(',')
                    for i in curline:
                        byte_n += 1
                        read_n += 1
                        image_data.append(int(i))
                        if h1 > 0 and byte_n == width * h_step * 2:
                            self.lcd_show_image(image_data, xs, ys, width, h_step)
                            image_data = []
                            ys = ys + h_step
                            h1 -= 1
                            byte_n = 0
                            # print('image_data len = {}'.format(len(image_data)))
                        elif h1 == 0 and read_n == width * heigth * 2:
                            if h2 != 0:
                                self.lcd_show_image(image_data, xs, ys, width, h2)

    '''
    ???24???????????????16??????
    ????????????24?????????0xFF0000??????r=0xFF,g=0x00,b=0x00,
    ???r???g???b????????????????????????????????????16?????????????????????
    '''
    def get_rgb565_color(self, r, g, b):
        return ((r << 8) & 0xF800) | ((g << 3) & 0x07E0) | ((b >> 3) & 0x001F)
