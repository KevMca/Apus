################################################################################
# BNO055.py
# The class wrapper for the BNO055 9 DOF IMU
#
# Author:  Kevin McAndrew
# Created: 21 July 2020
################################################################################
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

################################################################################
# An object representing the BNO055 9 DOF fusion 
# Initialise with constants and then use update function to update the PID
# controller with current error
#
#   Params: kp - proportional constant
#           ki - integral constant
#           kd - derivative constant
################################################################################
class BNO055:

    # --------------------------------------------------------------------------
    # Initialisation method
    # --------------------------------------------------------------------------
    def __init__(self, i2c_bus):
        # Setup i2c
        self.i2c = i2c_bus

        # Setup operation mode
        #self.i2c.writeto(addr_bosch, bytearray([REGISTER, DATA]))
        self.i2c.writeto(addr_bosch, b'\x3D\x0C', True)
    
    # --------------------------------------------------------------------------
    # Converts bytes read from BNO055 module into two's complement form and then 
    # converts into signed integer 
    # --------------------------------------------------------------------------
    def bytes_toint(self, bLow, bHigh):
        two_comp = (bHigh<<8) | bLow
        # If number is negative : MSB = 1
        if (two_comp & (1<<15)) != 0:
            two_comp = two_comp - (1 << 16)
        return two_comp

    # --------------------------------------------------------------------------
    # Read euler angles from the BNO055
    # Pitch : from -180 to +180
    # Roll  : from -90  to +90
    # Yaw   : from 0    to +360
    # --------------------------------------------------------------------------
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
            return Euler(-1, -1, -1)

    #def readQuat(self):
