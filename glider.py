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
import modes #config
import os, time, utime, ujson
from machine import I2C, Pin
# Import custom libraries
#try:
os.chdir('Lib')
import rc
from BNO055 import BNO055
from BMP180 import BMP180
from servo import servo
from pid import pid
from airspeed import airspeed
os.chdir('..')
#except:
#    print("Err : error importing libraries")

# --------------------------------------------------------------------------
# Setup
# --------------------------------------------------------------------------

# RC control pins
roll, pitch, throttle, yaw = 35, 34, 33, 32
VRA, VRB = 39, 36
receiver = rc.receiver([roll, pitch, throttle, yaw, VRA, VRB])

# Servo control pins
pitch_servo = servo(23)
roll_servo = servo(18, offset=-7)
yaw_servo = servo(19)
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
# Write to file
with open("/Web/www/autre.json", "r") as f:
    autre_file = ujson.load(f)
with open("/Web/www/autre.json", "w") as f:
    autre_file[2]["data"]["target"] = pitch_init
    autre_file[1]["data"]["target"] = roll_init
    ujson.dump(autre_file, f)

# Airspeed
speed = airspeed(bmp180)
speed_init = 10

# PID controllers
pitch_pid = pid(0, 0, 0)
roll_pid = pid(0, 0, 0)
speed_pid = pid(0, 0, 0)

# Read configuration
pid_counter = 0
#config.readConfig(pitch_pid, roll_pid, speed_pid)

# Setup mode object
mode = modes.mode(receiver, speed, bno055, speed_pid, pitch_pid, roll_pid,
                pitch_servo, roll_servo, throttle_servo, yaw_servo)

# --------------------------------------------------------------------------
# Main loop
# --------------------------------------------------------------------------

while(True):
    # Else if SWC is ON, PID control is on
    if receiver.time[4] >= 1500:
        mode.pidMode()
    
    # If SWC is OFF, then RC control is on
    elif receiver.time[4] < 1500:
        mode.rcMode()
