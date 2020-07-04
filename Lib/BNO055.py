# Import libraries
import time
from machine import I2C
from machine import Pin
from pygebra import Euler

# Addresses
addr_bosch = 41

# Registers
OPR_MODE        = b'\x3D'
EUL_Pitch_MSB   = b'\x1F'
EUL_Pitch_LSB   = b'\x1E'
EUL_Roll_MSB    = b'\x1D'
EUL_Roll_LSB    = b'\x1C'
EUL_Heading_MSB = b'\x1B'
EUL_Heading_LSB = b'\x1A'

# ----------------------------------------------- #
# BNO055(clock, data)
# An object representing the BNO055 9 DOF fusion 
# IMU. clock and data are the clk and sda pins for i2c 
# ----------------------------------------------- #
class BNO055:

    # Initialise the BNO055
    def __init__(self, clock = 22, data = 21):
        # Setup i2c
        self.i2c = I2C(scl=Pin(clock), sda=Pin(data))
        print(self.i2c.scan())

        # Setup operation mode
        self.i2c.writeto(addr_bosch, b'\x3D\x0C', True)

    # Setup device
    #def setup(self):
        #self.i2c.writeto(addr_bosch, bytearray([REGISTER, DATA]))
    
    # Converts bytes read from BNO055 module into two's complement
    # form and then converts into signed integer 
    def bytes_toint(self, bLow, bHigh):
        two_comp = (bHigh<<8) | bLow
        # If number is negative : MSB = 1
        if (two_comp & (1<<15)) != 0:
            two_comp = two_comp - (1 << 16)
        return two_comp

    # Read euler angles from the BNO055
    # Pitch : from -180 to +180
    # Roll  : from -90  to +90
    # Yaw   : from 0    to +360
    def readEuler(self):
        try:
            # Set register to read from
            self.i2c.writeto(addr_bosch, EUL_Heading_LSB, False)
            # Read 3 axes
            reading_byte = self.i2c.readfrom(addr_bosch, 6, True)
            reading = list(reading_byte)
            euler = Euler((self.bytes_toint(reading[4], reading[5])/16),\
                (self.bytes_toint(reading[2], reading[3])/16),\
                (self.bytes_toint(reading[0], reading[1])/16))
            return euler

        except:
            return -1

    def readQuat(self):

        
        
        

# from BNO055 import BNO055
# imu = BNO055()
# imu.readEuler()