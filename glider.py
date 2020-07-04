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
import os, utime
# Import custom libraries
try:
    os.chdir('Lib')
    import rc
    os.chdir('..')
except:
    print("Err : error importing rc")

# RC control pins
roll, pitch, throttle, yaw = 35, 34, 33, 32
VRA, VRB = 39, 36

# --------------------------------------------------------------------------
# Setup
# --------------------------------------------------------------------------

# Relay RC controls onto servos
rec = rc.receiver([roll, pitch, throttle, yaw, VRA, VRB])
