################################################################################
# modes.py
# Defines the flight modes available to the glider. It is imported into glider.py
# and each flight mode is run in the main loop. There are currently 2 modes.
#
# (1) RC mode  - Manual remote control from a controller
# (2) PID mode - Some manual control, with PID controllers on axes to guide the
#                glider
#
# Author:  Kevin McAndrew
# Created: 27 October 2020
################################################################################

#import config
import os
os.chdir('Lib')
import rc
os.chdir('..')

class mode:
    # --------------------------------------------------------------------------
    # Initialisation method
    # --------------------------------------------------------------------------
    def __init__(self, receiver, speed, bno055, speed_pid, pitch_pid, roll_pid, \
                pitch_servo, roll_servo, throttle_servo, yaw_servo):
        # Initialise inputs
        self.receiver = receiver
        self.speed = speed
        self.bno055 = bno055

        # Initialise PID controllers
        self.speed_pid = speed_pid
        self.pitch_pid = pitch_pid
        self.roll_pid = roll_pid

        # Initialise servos
        self.pitch_servo = pitch_servo
        self.roll_servo = roll_servo
        self.throttle_servo = throttle_servo
        self.yaw_servo = yaw_servo

        # Initialise rolling averages
        self.roll_avg = rc.movingAvg(10, 10)
        self.pitch_avg = rc.movingAvg(10, 7)
        self.yaw_avg = rc.movingAvg(10, 10)

        # Timing control
        self.pid_counter = 0

    # --------------------------------------------------------------------------
    # RC mode of operation
    # --------------------------------------------------------------------------
    def rcMode(self):  
        if self.receiver.new == 1:
            print('RC')
            # Reset new receiver flag
            self.receiver.new = 0

            # Roll
            roll_angle = self.roll_avg.update((self.receiver.time[0] - 990) * (180/1000))
            self.roll_servo.deg(roll_angle+6)
            # Pitch
            pitch_angle = self.pitch_avg.update((self.receiver.time[1] - 990) * (180/1000))
            self.pitch_servo.deg(pitch_angle)
            # Throttle
            throttle_angle = (self.receiver.time[2] - 990) * (180/1000)
            self.throttle_servo.deg(throttle_angle)
            # Yaw
            yaw_angle = self.yaw_avg.update((self.receiver.time[3] - 990) * (180/1000))
            self.yaw_servo.deg(yaw_angle)

    # --------------------------------------------------------------------------
    # PID mode of operation
    # --------------------------------------------------------------------------
    def pidMode(self):
        if self.receiver.new == 1:
            print('PID')
            # Reset new receiver flag
            self.receiver.new = 0

            # Read PID parameters - every second
            if(self.pid_counter == 50):
                self.pid_counter = 0
                # read JSON
                #config.readConfig(self.pitch_pid, self.roll_pid, self.speed_pid)
            else:
                self.pid_counter += 1

            # Pitch
            # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
            # Read sensors
            speed_read = self.speed.read()
            pitch_read = self.bno055.readEuler().angle_x
            # If readings are valid ...
            if pitch_read != -1 and pitch_read != 0:
                if speed_read != None and speed_read < 20:
                    self.speed_pid.update(self.speed_pid.initial - speed_read)
                # Remap pitch to better angles
                pitch_read = pitch_read+180 if pitch_read <= 0 else pitch_read-180
                # Update PID controller
                self.pitch_pid.update(self.pitch_pid.initial - pitch_read)
                # Set servo
                pitch_angle = self.pitch_pid.output + 90
                self.pitch_servo.deg(pitch_angle + self.speed_pid.output)

            # Roll
            # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
            # Read sensors
            roll_read = self.bno055.readEuler().angle_y
            # If readings are valid ...
            if roll_read != -1 and roll_read != 0 and roll_read != 4:
                # Update PID controller
                self.roll_pid.update(self.roll_pid.initial - roll_read)
                # Set servo
                roll_angle = self.roll_pid.output + 90
                self.roll_servo.deg(roll_angle)
