from machine import Pin
import dht
import json

# 对应模块针脚D15
dht22 = dht.DHT22(Pin(15))
dht22.measure()
print(dht22.temperature())
print(dht22.humidity())

d1 = {
    "temperature": dht22.temperature(),
    "humidity": dht22.humidity()
}

j1 = json.dumps(d1)
print(j1)
