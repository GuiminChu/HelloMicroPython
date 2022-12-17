import network
import time


class Wifi:
    wifi = network.WLAN(network.STA_IF)

    @classmethod
    def do_connect(cls) -> bool:
        if not cls.wifi.isconnected():
            cls.wifi.active(True)
            cls.wifi.connect("qnaiot", "qingniao2022")
            # cls.wifi.connect("Xiaomi_F285", "STC12C5A")

            for i in range(20):
                print('等待连接...{}'.format(i))
                if cls.wifi.isconnected():
                    print('network config:', cls.wifi.ifconfig())
                    break

                time.sleep(1)
        else:
            print('network config:', cls.wifi.ifconfig())

        return cls.wifi.isconnected()
