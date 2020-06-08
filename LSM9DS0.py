# Import libraries
from machine import I2C
from machine import Pin
from pygebra import Vector3

# Addresses
addr_gyro = 107
addr_accel_mag = 29

# Registers
CTRL_REG1_G = const(0x20)
CTRL_REG2_G = const(0x21)
CTRL_REG3_G = const(0x22)
CTRL_REG4_G = const(0x23)
CTRL_REG5_G = const(0x24)
CTRL_REG0_XM = const(0x1F)
CTRL_REG1_XM = const(0x20)
CTRL_REG2_XM = const(0x21)
CTRL_REG3_XM = const(0x22)
CTRL_REG4_XM = const(0x23)
CTRL_REG5_XM = const(0x24)
CTRL_REG6_XM = const(0x25)
CTRL_REG7_XM = const(0x26)
OUT_X_L_G = const(0x28)
OUT_X_L_M = const(0x08)
OUT_X_L_A = const(0x28)

# Accelerometer
a_rate_3Hz = const(0b0001)
a_rate_6Hz = const(0b0010)
a_rate_12Hz = const(0b0011)
a_rate_25Hz = const(0b0100)
a_rate_50Hz = const(0b0101)
a_rate_100Hz = const(0b0110)
a_rate_200Hz = const(0b0111)
a_rate_400Hz = const(0b1000)
a_rate_800Hz = const(0b1001)
a_rate_1600Hz = const(0b1010)
a_2g = const(0b000)
a_4g = const(0b001)
a_6g = const(0b010)
a_8g = const(0b011)
a_16g = const(0b100)

# Magnetometer
m_rate_3Hz = const(0b000)
m_rate_6Hz = const(0b001)
m_rate_12Hz = const(0b010)
m_rate_25Hz = const(0b011)
m_rate_50Hz = const(0b100)
m_rate_100Hz = const(0b101)
m_2g = const(0b00)
m_4g = const(0b01)
m_8g = const(0b10)
m_12g = const(0b11)

# Gyro
g_rate_95Hz = const(0b00)
g_rate_190Hz = const(0b01)
g_rate_380Hz = const(0b10)
g_rate_760Hz = const(0b11)
g_cut_12 = const(0b00)
g_cut_25 = const(0b01)
g_cut_50 = const(0b10)
g_cut_70 = const(0b11)

# ----------------------------------------------- #
# lsm9ds0(clock, data)
# An object representing the LSM9DS0 9 DOF IMU. clock
# and data are the clk and sda pins for i2c 
# ----------------------------------------------- #
class lsm9ds0:
    
    # Initialise the lsm9ds0
    def __init__(self, clock = 22, data = 21):
        # Setup i2c
        self.i2c = I2C(scl=Pin(clock), sda=Pin(data))
        print(self.i2c.scan())
        # Set the min and max calibrated magnetometor readings
        self.mag_min = [-0.618042, -1.426025, -0.7663574]
        self.mag_max = [0.44104, -0.6049805, 0.5472412]

        # Setup device control registers over i2c
        try:
            self.setupAcc()
        except:
            print("Error setting up Acc - Check addresses")
        try:
            self.setupMag()
        except:
            print("Error setting up Mag - Check addresses")
        try:
            self.setupGyro()
        except:
            # Change address and try again
            print("address is not 107")
            addr_gyro = 105
            try:
                self.setupGyro()
            except:
                print("Error setting up Gyro - Check addresses")
            
    # -----------------Functions----------------- #
    # Accelerometer setup
    def setupAcc(self):
        # 100Hz, continuous update, axes enabled
        self.i2c.writeto(addr_accel_mag, bytearray([CTRL_REG1_XM, (a_rate_100Hz<<4) | 0b111]))
        # full-scale 4g, all else DEFAULT
        self.i2c.writeto(addr_accel_mag, bytearray([CTRL_REG2_XM, (a_4g<<3)]))
    
    # Magnetometer setup
    def setupMag(self):
        # High resolution, 100Hz refresh, temp disabled
        self.i2c.writeto(addr_accel_mag, bytearray([CTRL_REG5_XM, (0b11<<5) | (m_rate_100Hz<<2)]))
        # 4 gauss full scale
        self.i2c.writeto(addr_accel_mag, bytearray([CTRL_REG6_XM, (m_2g<<5)]))
        # Turn on module
        self.i2c.writeto(addr_accel_mag, bytearray([CTRL_REG7_XM, 0]))

    # Gyro setup
    def setupGyro(self):
        # 380Hz refresh rate, 25 cutoff, turn on module
        self.i2c.writeto(addr_gyro, bytearray([CTRL_REG1_G, (g_rate_380Hz<<6) | (g_cut_25<<4) | 0b1111]))

    # Converts bytes read from LSM9DS0 module into two's complement
    # form and then converts into signed integer 
    def bytes_toint(self, bLow, bHigh):
        two_comp = (bHigh<<8) | bLow
        # If number is negative : MSB = 1
        if (two_comp & (1<<15)) != 0:
            two_comp = two_comp - (1 << 16)
        return two_comp
    
    # Does a hard iron calibration, where the min and max magnetometer
    # readings are updated along each axis
    def hardIron(self, magReading):
        if magReading[0] < self.mag_min[0]:
            self.mag_min[0] = magReading[0]
        if magReading[0] > self.mag_max[0]:
            self.mag_max[0] = magReading[0]
        if magReading[1] < self.mag_min[1]:
            self.mag_min[1] = magReading[1]
        if magReading[1] > self.mag_max[1]:
            self.mag_max[1] = magReading[1]
        if magReading[2] < self.mag_min[2]:
            self.mag_min[2] = magReading[2]
        if magReading[2] > self.mag_max[2]:
            self.mag_max[2] = magReading[2]

    # Reads the magnetometer and returns a vector of pointing in the
    # direction of North
    def readMag(self, calib = True):
        # OUT_X_L_A register has MSB set so that the pointer auto-increments
        # Read 6 bytes after OUT_X_L_A / 2 bytes per axis
        reading = self.i2c.readfrom_mem(addr_accel_mag, OUT_X_L_M | 0x80, 6)
        # Assuming 4g full scale deflection
        magReading = [((self.bytes_toint(reading[0], reading[1]) * 4) / 32768),
            ((self.bytes_toint(reading[2], reading[3]) * 4) / 32768),
            ((self.bytes_toint(reading[4], reading[5]) * 4) / 32768)]

        #Calibration
        if calib == True:
            self.hardIron(magReading)
        # Centre around 0
        magReading = [(a - (mx + mn)/2) for a, mx, mn in zip(magReading, self.mag_max, self.mag_min)]
        # Normalise
        try:
            magReading = [(a / ((mx - mn)/2)) for a, mx, mn in zip(magReading, self.mag_max, self.mag_min)]
        except:
            print()

        return Vector3.from_vect(magReading)

    # Reads the accelerometer and returns a vector of pointing in the
    # direction of the force on the device
    def readAcc(self):
        # OUT_X_L_A register has MSB set so that the pointer auto-increments
        # Read 6 bytes after OUT_X_L_A / 2 bytes per axis
        reading = self.i2c.readfrom_mem(addr_accel_mag, OUT_X_L_A | 0x80, 6)
        # Assuming 4g full scale deflection
        accReading = [-((self.bytes_toint(reading[0], reading[1]) * 4) / 32768),
            (-(self.bytes_toint(reading[2], reading[3]) * 4) / 32768),
            ((self.bytes_toint(reading[4], reading[5]) * 4) / 32768)]

        return Vector3.from_vect(accReading)

    # Reads the gyroscope and returns angular rates for each axis
    def readGyro(self):
        # OUT_X_L_G register has MSB set so that the pointer auto-increments
        # Read 6 bytes after OUT_X_L_A / 2 bytes per axis
        reading = self.i2c.readfrom_mem(addr_gyro, OUT_X_L_G | 0x80, 6)
        # Assuming 245 degrees per second full scale deflection
        gyroReading = [-((self.bytes_toint(reading[0], reading[1]) * 245) / 32768),
            (-(self.bytes_toint(reading[2], reading[3]) * 245) / 32768),
            ((self.bytes_toint(reading[4], reading[5]) * 245) / 32768)]

        return Vector3.from_vect(gyroReading)