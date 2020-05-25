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

def orient():
    down = imu.readAcc()
    down.norm()
    mag = imu.readMag()
    # Find west and normalise
    west = down.cross(mag)
    west.norm()
    # Find North and normalise
    north = down.cross(west)
    north.norm()
    return Matrix(west, north, down)

def orientEuler():
    while True:
        m = orient()
        e = m.toEuler()
        e.toDeg()
        print(e)
        time.sleep_ms(10)

def northCont():
    while True:
        down = imu.readAcc()
        down.norm()
        mag = imu.readMag()
        # Find west and normalise
        west = down.cross(mag)
        west.norm()
        # Find North and normalise
        north = west.cross(down)
        north.norm()
        print(north)
        time.sleep_ms(10)

def mag():
    #while True:
    mag = imu.readMag()
    return mag
    #print(mag)
    #time.sleep_ms(10)

def acc():
    while True:
        acc = imu.readAcc()
        print(acc)
        time.sleep_ms(10)

def iron():
    imu.mag_min = list((4, 4, 4))
    imu.mag_max = list((-4, -4, -4))
    while True:
        mag = imu.readMag()
        print('Min: {}   Max: {}'.format(imu.mag_min, imu.mag_max))

