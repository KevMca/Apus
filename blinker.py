# Used to blink the 
print('LOAD: blinker.py')

from machine import Pin
import time

def blink(pin = 5):
    led = Pin(pin, Pin.OUT)

    try:
        while True:
            led.value(not led.value())
            time.sleep_ms(100)

    except:
        led.value(0)
        Pin(pin,Pin.IN)