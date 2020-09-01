################################################################################
# pid.py
# The class wrapper for pid controllers
#
# Author:  Kevin McAndrew
# Created: 5 July 2020
################################################################################
# Import libraries
from machine import Pin
from machine import UART
import time, utime, math

################################################################################
# Generic PID class for controlling surfaces
# Initialise with constants and then use update function to update the PID
# controller with current error
#
#   Params: kp - proportional constant
#           ki - integral constant
#           kd - derivative constant
################################################################################
class airspeed:
    # --------------------------------------------------------------------------
    # Initialisation method
    # --------------------------------------------------------------------------
    def __init__(self, bmp, baud=115200, tx=17, rx=16):
        self.bmp = bmp
        self.uart = UART(1,baud,tx=tx,rx=rx)
        #self.std_p = 101655
        # Calculate pressure offset
        while(True):
            reading = self.uart.read()
            if reading == None:
                continue
            else:
                pressure = self.readPressure(reading)
                break
        self.std_p = self.bmp.pressure - pressure
        self.density = 1.225

    # --------------------------------------------------------------------------
    # Read the airspeed from the airspeed sensor
    # --------------------------------------------------------------------------
    def read(self):
        reading = self.uart.read()
        if(reading == None):
            return None
        pressure = self.readPressure(reading)
        temp = self.readTemp(reading)
        speed = math.sqrt(abs( (2*(pressure - 102087.3 + self.std_p)) / self.density) )

        return speed
    
    def readPressure(self, reading):
        return reading[4] \
            + (reading[5] << 8) \
            + (reading[6] << 16) \
            + (reading[7] << 24)

    def readTemp(self, reading):
        return reading[8] \
            + (reading[9] << 8) \
            + (reading[10] << 16) \
            + (reading[11] << 24)
    

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