################################################################################
# glider.py
# Main file to be run be the Lidl glider.
#
# Author:  Kevin McAndrew
# Created: 30 June 2020
################################################################################

# --------------------------------------------------------------------------
# Import libraries
# --------------------------------------------------------------------------
import os, time, utime
from machine import I2C, Pin
# Import custom libraries
#try:
os.chdir('Lib')
import rc
from BNO055 import BNO055
from BMP180 import BMP180
from servo import servo
from pid import pid
os.chdir('..')
#except:
#    print("Err : error importing libraries")

# --------------------------------------------------------------------------
# Setup
# --------------------------------------------------------------------------

# RC control pins
roll, pitch, throttle, yaw = 35, 34, 33, 32
VRA, VRB = 39, 36
rec = rc.receiver([roll, pitch, throttle, yaw, VRA, VRB])

# Servo control pins
pitch_servo = servo(19)
roll_servo = servo(23, offset=-7)
yaw_servo = servo(18)
throttle_servo = servo(5)

# I2C
I2C_bus = I2C(scl=Pin(22), sda=Pin(21))

# bmp180
bmp180 = BMP180(I2C_bus)
bmp180.oversample_sett = 2
bmp180.baseline = 101325
alt_init = bmp180.altitude

# BNO055
bno055 = BNO055(I2C_bus)
pitch_init = bno055.readEuler().angle_x
pitch_init = pitch_init+180 if pitch_init <= 0 else pitch_init-180
roll_init = bno055.readEuler().angle_y

# PID controllers
pitch_pid = pid(1, 0, 0)
roll_pid = pid(-1, 0, 0)
p_avg = rc.movingAvg(50)
i_avg = rc.movingAvg(50)
d_avg = rc.movingAvg(50)

# --------------------------------------------------------------------------
# Main loop
# --------------------------------------------------------------------------

roll_avg = rc.movingAvg(10)
pitch_avg = rc.movingAvg(10)
yaw_avg = rc.movingAvg(10)

while(True):
    '''# If SWC is off, then RC control is on
    if rec.time[4] < 1500:
        # Move servos to receiver value
        if rec.new == 1:
            rec.new = 0
            # Roll
            roll_angle = roll_avg.update((rec.time[0] - 990) * (180/1000))
            roll_servo.deg(roll_angle)
            # Pitch
            pitch_angle = pitch_avg.update((rec.time[1] - 990) * (180/1000))
            pitch_servo.deg(pitch_angle)
            # Throttle
            throttle_angle = yaw_avg.update((rec.time[2] - 990) * (180/1000))
            throttle_servo.deg(throttle_angle)
            # Yaw
            yaw_angle = (rec.time[3] - 990) * (180/1000)
            yaw_servo.deg(yaw_angle)
    # Else if SWC is on, PID control is on
    else:'''
    if rec.new == 1:
        rec.new = 0
        ### MAKE INTO OWN PROGRAM ###
        # Pitch
        # PID parameters
        pitch_pid.kp = p_avg.update((rec.time[5] - 990) * (-5/1000))
        pitch_pid.ki = i_avg.update((rec.time[4] - 990) * (-1/1000))
        pitch_pid.kd = d_avg.update((rec.time[2] - 990) * (-0.5/1000))
        #print("p: {:.5f}, i: {:.5f}, d: {:.5f}".format(pitch_pid.kp, pitch_pid.ki, pitch_pid.kd))
        # Error control
        pitch_read = bno055.readEuler().angle_x
        if pitch_read != -1 and pitch_read != 0:
            # Remap pitch to better angles
            pitch_read = pitch_read+180 if pitch_read <= 0 else pitch_read-180
            # Update PID controller
            pitch_pid.update(pitch_init - pitch_read)
            # Set servo
            pitch_angle = pitch_pid.output + 90
            pitch_servo.deg(pitch_angle)
            #print("pitch: {}".format(pitch_angle))

        # Roll
        # Error control
        roll_read = bno055.readEuler().angle_y
        if roll_read != -1 and roll_read != 0 and roll_read != 4:
            # Update PID controller
            roll_pid.update(roll_init - roll_read)
            # Set servo
            roll_angle = roll_pid.output + 90
            roll_servo.deg(roll_angle)
            #print("roll_read: {}".format(roll_read))

