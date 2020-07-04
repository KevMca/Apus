from machine import Pin
from machine import UART
import time, utime, math

uart = UART(1,baudrate=115200,tx=17,rx=16)
std_p = 101655
density = 1.225

def read():
    reading = uart.read()
    pressure = reading[4] \
        + (reading[5] << 8) \
        + (reading[6] << 16) \
        + (reading[7] << 24)
    print("pressure: {}".format(pressure))
    temp = reading[8] \
        + (reading[9] << 8) \
        + (reading[10] << 16) \
        + (reading[11] << 24)
    print("temp: {}".format(temp))
    speed = math.sqrt(abs( (2*(pressure - std_p)) / density) )
    print("speed: {}".format(speed))

# 102087.3 kPa

#prev_time = utime.ticks_us()

#def pin_handle(pin):
#    global prev_time
#    print(utime.ticks_diff(utime.ticks_us(), prev_time))
#    prev_time = utime.ticks_us()

#p17 = Pin(17, Pin.OUT)
#p17.off()

#p16 = Pin(16, Pin.IN)
#p16.irq(pin_handle)