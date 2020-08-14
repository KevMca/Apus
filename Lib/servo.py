################################################################################
# servo.py
# The class wrapper for servos
#
# Author:  Kevin McAndrew
# Created: 5 July 2020
################################################################################
# Import libraries
from machine import Pin
from machine import PWM

servo_max = 130
servo_min = 40

################################################################################
# Servo class for pitch, roll and yaw controls
#
# 
#
#   Params: pin - the PWM pin for the servo
#           min_deg - the minimum angle in degrees
#           max_deg - the maximum angle in degrees
#           offset - the offset angle to zero servos
################################################################################
class servo:
    # --------------------------------------------------------------------------
    # Initialisation method
    # --------------------------------------------------------------------------
    def __init__(self, pin, min_deg=0, max_deg=180, offset=0):
        self.PWM = PWM(Pin(pin, Pin.OUT), freq=50)
        self.curr_angle = 0
        self.min_deg = min_deg
        self.max_deg = max_deg
        self.offset = offset
    
    # --------------------------------------------------------------------------
    # Move servo to an angle in degrees
    # --------------------------------------------------------------------------
    def deg(self, angle):
        if angle < self.min_deg or angle > self.max_deg:
            #print("err: servo instructed beyond maximum angle")
            return
        else:
            self.curr_angle = angle
            duty = ((angle/180) * (servo_max-servo_min)) + servo_min + self.offset
            self.PWM.duty(int(duty))
