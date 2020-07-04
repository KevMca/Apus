# Import I2C library
import time
from machine import I2C
from machine import Pin
from LSM9DS0 import lsm9ds0
from pygebra import Vector3
from pygebra import Matrix
from pygebra import Euler

# create I2C peripheral at frequency of 400kHz
# depending on the port, extra parameters may be required
# to select the peripheral and/or pins to use
imu = lsm9ds0()

def complementary():
    while(True):
        imu.complFilter()
        print(imu.angle)

def iron():
    imu.mag_min = list((4, 4, 4))
    imu.mag_max = list((-4, -4, -4))
    while True:
        mag = imu.readMag()
        print('Min: {}   Max: {}'.format(imu.mag_min, imu.mag_max))

