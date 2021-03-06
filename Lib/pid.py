################################################################################
# pid.py
# The class wrapper for pid controllers
#
# Author:  Kevin McAndrew
# Created: 5 July 2020
################################################################################
# Import libraries
import utime, servo

################################################################################
# Generic PID class for controlling surfaces
# Initialise with constants and then use update function to update the PID
# controller with current error
#
#   Params: kp - proportional constant
#           ki - integral constant
#           kd - derivative constant
################################################################################
class pid:
    # --------------------------------------------------------------------------
    # Initialisation method
    # --------------------------------------------------------------------------
    def __init__(self, kp, ki, kd, initial = 0):
        # Constants
        self.params = {"kp": kp, "ki": ki, "kd": kd}
        # Maximum
        self.max = 90
        self.min = -90
        # Other variables
        self.initial = initial
        self.integral = 0
        self.prev_err = 0
        self.prev_time = utime.ticks_us()
        self.output = 0

    # --------------------------------------------------------------------------
    # Update the PID controller with the current error
    # --------------------------------------------------------------------------
    def update(self, error):
        # Calculate dt
        curr_time = utime.ticks_us()
        dt = float(utime.ticks_diff(curr_time, self.prev_time))/float(1000000)

        # Calculate proportional
        Pout = self.params["kp"] * error
        
        # Calculate integral
        self.integral += error * dt
        Iout = self.params["ki"] * self.integral

        # Calculate derivative
        derivative = (error - self.prev_err) / dt
        Dout = self.params["kd"] * derivative

        '''print("------------------------------------")
        print("Pout {} | Iout {} | Dout {}".format(Pout, Iout, Dout))
        print("kp   {} | ki   {} | kd   {}".format(self.params["kp"], self.params["ki"], self.params["kd"]))
        print("------------------------------------")'''

        self.output = Pout + Iout + Dout

        # Apply maximums to output with anti windup
        if(self.output > self.max):
            self.output = self.max
            # Anti-windup
            self.integral -= error * dt
        elif(self.output < self.min):
            self.output = self.min
            # Anti-windup
            self.integral -= error * dt
        
        # Save error
        self.prev_err = error
        self.prev_time = utime.ticks_us()
