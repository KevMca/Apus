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
pid_counter = 0
pitch_pid = pid(0, 0, 0)
roll_pid = pid(0, 0, 0)
speed_pid = pid(0, 0, 0)

# --------------------------------------------------------------------------
# Helper functions
# --------------------------------------------------------------------------

def readConfig():
    with open("/Web/www/pid.json", "r") as f:
        json_file = ujson.load(f)
        global pitch_pid, roll_pid, speed_pid
        # Assign parameters
        # Pitch
        if pitch_pid.params["ki"] != float(json_file[0]["data"]["i"]):
            pitch_pid.integral = 0
        pitch_pid.params["kp"] = float(json_file[0]["data"]["p"])
        pitch_pid.params["ki"] = float(json_file[0]["data"]["i"])
        pitch_pid.params["kd"] = float(json_file[0]["data"]["d"])
        # Roll
        if roll_pid.params["ki"] != float(json_file[1]["data"]["i"]):
            roll_pid.integral = 0
        roll_pid.params["kp"] = float(json_file[1]["data"]["p"])
        roll_pid.params["ki"] = float(json_file[1]["data"]["i"])
        roll_pid.params["kd"] = float(json_file[1]["data"]["d"])
        # Speed
        if speed_pid.params["ki"] != float(json_file[2]["data"]["i"]):
            speed_pid.integral = 0
        speed_pid.params["kp"] = float(json_file[2]["data"]["p"])
        speed_pid.params["ki"] = float(json_file[2]["data"]["i"])
        speed_pid.params["kd"] = float(json_file[2]["data"]["d"])
    with open("/Web/www/autre.json", "r") as f:
        json_file = ujson.load(f)
        # Assign parameters
        global speed_init, pitch_init, roll_init
        speed_init= float(json_file[0]["data"]["target"])
        pitch_init = float(json_file[2]["data"]["target"])
        roll_init = float(json_file[1]["data"]["target"])

# Read configuration
readConfig()

# --------------------------------------------------------------------------
# Main loop
# --------------------------------------------------------------------------

while(True):
    # Else if SWC is on, PID control is on
    #if rec.time[4] >= 1500:
    if rec.new == 1:
        rec.new = 0
        # Pitch
        # PID parameters - every second
        if(pid_counter == 50):
            pid_counter = 0
            # read JSON
            readConfig()
        else:
            pid_counter += 1

        # Error control
        # Pitch
        speed_read = speed.read()
        pitch_read = bno055.readEuler().angle_x
        if pitch_read != -1 and pitch_read != 0:
            if speed_read != None and speed_read < 20:
                speed_pid.update(speed_init - speed_read)
            # Remap pitch to better angles
            pitch_read = pitch_read+180 if pitch_read <= 0 else pitch_read-180
            # Update PID controller
            pitch_pid.update(pitch_init - pitch_read)
            # Set servo
            pitch_angle = pitch_pid.output + 90
            pitch_servo.deg(pitch_angle + speed_pid.output)

        # Roll
        roll_read = bno055.readEuler().angle_y
        if roll_read != -1 and roll_read != 0 and roll_read != 4:
            # Update PID controller
            roll_pid.update(roll_init - roll_read)
            # Set servo
            roll_angle = roll_pid.output + 90
            roll_servo.deg(roll_angle)
    '''
    # If SWC is off, then RC control is on
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
            yaw_servo.deg(yaw_angle)'''
