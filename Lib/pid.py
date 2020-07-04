import utime, servo
from LSM9DS0 import lsm9ds0

class pid:
    def __init__(self, kp, ki, kd):
        # Constants
        self.kp = kp
        self.ki = ki
        self.kd = kd
        # Maximum
        self.max = 90
        self.min = -90
        # Other variables
        self.integral = 0
        self.prev_err = 0
        self.prev_time = utime.ticks_us()
        self.output = 0

    def update(self, error):
        # Calculate dt
        curr_time = utime.ticks_us()
        dt = float(utime.ticks_diff(curr_time, self.prev_time))/float(1000000)

        # Calculate proportional
        Pout = self.kp * error
        
        # Calculate integral
        self.integral += error * dt
        Iout = self.ki * self.integral

        # Calculate derivative
        derivative = (error - self.prev_err) / dt
        Dout = self.kd * derivative

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

def test():
    imu = lsm9ds0()
    pid_i = pid(0.25, 0.5, 0.5)

    while(True):
        imu.complFilter()
        pid_i.update(0-imu.angle.angle_x)
        servo.servoDeg(pid_i.output + 90)
        print(pid_i.output)
