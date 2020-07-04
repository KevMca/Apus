# Import I2C library
from machine import I2C
from machine import Pin
import math

class mpu6050:
    
    def __init__(self, i2c, addr = 0x68):
        self.ACCEL_XOUT_H = 0x3B
        self.PWR_MGMT_1 = 0x6B
        self.i2c = i2c
        self.addr = addr

        # Write 0 to PWR_MGMT_1 to initialise
        self.i2c.writeto(addr, bytearray([self.PWR_MGMT_1, 0]))

    def read(self):
        # starting with register 0x3B (ACCEL_XOUT_H),
        # read 7 regs accel[x,y,z], gyro[x,y,z] and temp
        reading = self.i2c.readfrom_mem(self.addr, self.ACCEL_XOUT_H, 14)
        return reading
    
    def bytes_toint(self, b1, b2):
        if not b1 & 0x80:
            return b1 << 8 | b2
        return - (((b1 ^ 255) << 8) | (b2 ^ 255) + 1)

    def readAll(self):
        reading = self.read()
        out = {}
        out["Ax"] = self.bytes_toint(reading[0], reading[1])
        out["Ay"] = self.bytes_toint(reading[2], reading[3])
        out["Az"] = self.bytes_toint(reading[4], reading[5])
        out["Gx"] = self.bytes_toint(reading[8], reading[9])
        out["Gy"] = self.bytes_toint(reading[10], reading[11])
        out["Gz"] = self.bytes_toint(reading[12], reading[13])
        out["temp"] = self.bytes_toint(reading[6], reading[7]) / 340.00 + 36.53

        return out

    def readAcc(self):
        reading = self.read()
        accReading = {}
        accReading["x"] = self.bytes_toint(reading[0], reading[1])
        accReading["y"] = self.bytes_toint(reading[2], reading[3])
        accReading["z"] = self.bytes_toint(reading[4], reading[5])

        return accReading
    
    def readGyro(self):
        reading = self.read()
        gyroReading = {}
        gyroReading["x"] = self.bytes_toint(reading[8], reading[9])
        gyroReading["y"] = self.bytes_toint(reading[10], reading[11])
        gyroReading["z"] = self.bytes_toint(reading[12], reading[13])

        return gyroReading
    
    def readTemp(self):
        reading = self.read()
        temp = self.bytes_toint(reading[6], reading[7]) / 340.00 + 36.53

        return temp
    
    def anglesQuat(self):
        reading = self.readAll()
        norm = math.sqrt(math.pow(reading["Ax"],2) + math.pow(reading["Ay"],2) + math.pow(reading["Az"],2))
        accelQ = {}
        accelQ["w"] = 0
        accelQ["x"] = reading["Ax"] / norm
        accelQ["y"] = reading["Ay"] / norm
        accelQ["z"] = reading["Az"] / norm
        return accelQ

    def anglesRad(self):
        inQ = self.anglesQuat()
        accelR = {}
        # roll (x-axis rotation)
        sinr_cosp = 2 * (inQ["w"] * inQ["x"] + inQ["y"] * inQ["z"])
        cosr_cosp = 1 - 2 * (inQ["x"] * inQ["x"] + inQ["y"] * inQ["y"])
        accelR["roll"] = math.atan2(sinr_cosp, cosr_cosp)
        
        # pitch (y-axis rotation)
        sinp = 2 * (inQ["w"] * inQ["y"] - inQ["z"] * inQ["x"])
        if (sinp >= 1):
            accelR["pitch"] = (math.pi)/2
        elif (sinp <= -1):
            accelR["pitch"] = -((math.pi)/2)
        else:
            accelR["pitch"] = math.asin(sinp)
        
        # yaw (z-axis rotation)
        siny_cosp = 2 * (inQ["w"] * inQ["z"] + inQ["x"] * inQ["y"])
        cosy_cosp = 1 - 2 * (inQ["y"] * inQ["y"] + inQ["z"] * inQ["z"])
        accelR["yaw"] = math.atan2(siny_cosp, cosy_cosp)

        return accelR

    def anglesDeg(self):
        accelR = self.anglesRad()
        accelD = {}
        accelD["pitch"] = accelR["pitch"] * (180/math.pi)
        accelD["roll"] = accelR["roll"] * (180/math.pi)
        accelD["yaw"] = accelR["yaw"] * (180/math.pi)

        return accelD
