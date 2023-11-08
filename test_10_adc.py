from machine import Pin, ADC
from time import sleep

adc_pot = ADC(Pin(34))
adc_pot.atten(ADC.ATTN_11DB)  # 这里配置测量量程为3.3V
adc_pot.width(ADC.WIDTH_10BIT)

while True:
    pot_value = adc_pot.read()
    print(pot_value)
    sleep(1)
