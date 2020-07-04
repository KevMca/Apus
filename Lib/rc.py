################################################################################
# rc.py
# Reads the FS-R6B RC receiver by Flysky which outputs a PWM signal for servos
# which can be read by the ESP32.
#
# Author:  Kevin McAndrew
# Created: 25 June 2020
################################################################################
# Import libraries
import machine, utime
from machine import Pin

################################################################################
# Receiver class for the RC receiver
#
# Read self.time for final time values
#
# update() method acts as a handler for anytime a PWM signal triggers its pin.
# START is always the first pin to rise and END is always the last pin to rise.
# The fact that pins fire sequentially (the falling edge of one pulse is at the
# same time as the next pulse) is used in the IRQ.
#
#   Params: pins - list of pin numbers [START, ... , END]
#                  order is important!
################################################################################
class receiver:
    # --------------------------------------------------------------------------
    # Initialisation method
    # --------------------------------------------------------------------------
    def __init__(self, pins):
        # Initialise pins for trig on RISING 
        self.pins = {}
        for p in range(0, len(pins)-1):
            self.pins[pins[p]] = Pin(pins[p], Pin.IN, Pin.PULL_DOWN)
            self.pins[pins[p]].irq(handler=self.update, trigger=Pin.IRQ_RISING)
        
        # Setup last pin to trig on RISING and FALLING
        lastPin = pins[len(pins)-1]
        self.pins[lastPin] = Pin(lastPin, Pin.IN, Pin.PULL_DOWN)
        self.pins[lastPin].irq(handler=self.update, trigger=(Pin.IRQ_RISING | Pin.IRQ_FALLING))

        # Initialise other variables
        self.nPins = len(self.pins)
        self.time = [0]*self.nPins
        self.i = 0
        self.prevTime = utime.ticks_us()

    # --------------------------------------------------------------------------
    # The ISR for any pin interrupt
    # pin is of type Pin()
    # --------------------------------------------------------------------------
    def update(self, pin):
        # If it is the START
        if self.i == 0:
            self.prevTime = utime.ticks_us()
            self.i += 1
        else:
            # Read current time and find difference
            currTime = utime.ticks_us()
            self.time[self.i-1] = utime.ticks_diff(currTime, self.prevTime)
            
            # If not at the end - increment and save time
            if self.i != self.nPins:
                self.i += 1
                self.prevTime = currTime
            
            # END - increment overflow
            else:
                self.i = 0
                print(self.time)
            