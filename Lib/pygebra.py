################################################################################
# BNO055.py
# The class wrapper for the BNO055 9 DOF IMU
#
# Author:  Kevin McAndrew
# Created: 21 July 2020
################################################################################
# Import libraries
import math

################################################################################
# Vector3 takes either x, y, z coords using the .from_xyz(x, y, z) or 
# .from_vect(vect) class methods
# X, y, z values are stored in Vector3.vect
################################################################################
class Vector3:
    # --------------------------------------------------------------------------
    # Initialisation method
    # --------------------------------------------------------------------------
    def __init__(self, vect):
        self.vect = vect
    
    # --------------------------------------------------------------------------
    # Create a Vector3 object from x, y, z coordinates
    # eg. Vector3.from_xyz(1, 2, 1)
    # --------------------------------------------------------------------------
    @classmethod
    def from_xyz(cls, x, y, z):
        return cls([x, y, z])
    
    # --------------------------------------------------------------------------
    # Create a Vector3 object from an x, y, z array
    # eg. Vector3.from_vect([1, 2, 1])
    # --------------------------------------------------------------------------
    @classmethod
    def from_vect(cls, vect):
        return cls(vect)

    # --------------------------------------------------------------------------
    # Define test and print characteristics
    # --------------------------------------------------------------------------
    def __repr__(self):
        return "[x: {}, y: {}, z: {}]".format(self.vect[0], self.vect[1], self.vect[2])

    def __str__(self):
        return "[x: {}, y: {}, z: {}]".format(self.vect[0], self.vect[1], self.vect[2])

    # --------------------------------------------------------------------------
    # Finds cross product between the current vector 
    # (from the left) and c_vect (from the right)
    # --------------------------------------------------------------------------
    def cross(self, c_vect):
        c = Vector3.from_vect(
            [self.vect[1]*c_vect.vect[2] - self.vect[2]*c_vect.vect[1],
            self.vect[2]*c_vect.vect[0] - self.vect[0]*c_vect.vect[2],
            self.vect[0]*c_vect.vect[1] - self.vect[1]*c_vect.vect[0]])
        return c

    # --------------------------------------------------------------------------
    # Vector addition between current vect and a_vect
    # --------------------------------------------------------------------------
    def add(self, a_vect):
        return Vector3.from_vect([(a+b) for a, b in zip(self.vect, a_vect.vect)])

    # Normalises the current vector
    def norm(self):
        normal = math.sqrt( sum(math.pow(a, 2) for a in self.vect) )
        if normal == 0:
            self.vect = [0, 0, 0]
            return
        else:
            self.vect = [(a/normal) for a in self.vect]
            return

################################################################################
# Euler(angle_x, angle_y, angle_z)
# Euler takes three angles, pitch, roll and yaw or
# x, y, z
################################################################################
class Euler:
    # --------------------------------------------------------------------------
    # Initialisation method
    # --------------------------------------------------------------------------
    def __init__(self, angle_x, angle_y, angle_z):
        self.angle_x = angle_x
        self.angle_y = angle_y
        self.angle_z = angle_z
    
    # --------------------------------------------------------------------------
    # Define test and print characteristics
    # --------------------------------------------------------------------------
    def __repr__(self):
        return "[x: {}, y: {}, z: {}]".format(self.angle_x, self.angle_y, self.angle_z)

    def __str__(self):
        return "[x: {}, y: {}, z: {}]".format(self.angle_x, self.angle_y, self.angle_z)

    # --------------------------------------------------------------------------
    # Addition definition for euler angles
    # --------------------------------------------------------------------------
    def __add__(self, other):
        return Euler(self.angle_x + other.angle_x,\
                    self.angle_y + other.angle_y,
                    self.angle_z + other.angle_z)
    
    # --------------------------------------------------------------------------
    # Multiplication definition for euler angles
    # --------------------------------------------------------------------------
    def __mul__(self, other):
        try:
            return Euler(self.angle_x * other.angle_x,\
                self.angle_y * other.angle_y,
                self.angle_z * other.angle_z)
        except:
            return Euler(self.angle_x * other,\
                self.angle_y * other,
                self.angle_z * other)
    
    __rmul__ = __mul__

    # --------------------------------------------------------------------------
    # Convert from radians to degrees
    # --------------------------------------------------------------------------
    def toDeg(self):
        self.angle_x *= (180/math.pi)
        self.angle_y *= (180/math.pi)
        self.angle_z *= (180/math.pi)

    # --------------------------------------------------------------------------
    # Convert from degrees to radians
    # --------------------------------------------------------------------------
    def toRad(self):
        self.angle_x *= (math.pi/180)
        self.angle_y *= (math.pi/180)
        self.angle_z *= (math.pi/180)

################################################################################
# Matrix(vectx, vecty, vectz)
# Matrix takes three Vector3 vectors that represent 
# the change of basis vectors
################################################################################
class Matrix:
    # --------------------------------------------------------------------------
    # Initialisation method
    # --------------------------------------------------------------------------
    def __init__(self, vect_x, vect_y, vect_z):
        self.vect_x = vect_x
        self.vect_y = vect_y
        self.vect_z = vect_z
    
    # --------------------------------------------------------------------------
    # Define test and print characteristics
    # --------------------------------------------------------------------------
    def __repr__(self):
        return "x{}; y{}; z{}".format(self.vect_x, self.vect_y, self.vect_z)

    def __str__(self):
        return "x{}; y{}; z{}".format(self.vect_x, self.vect_y, self.vect_z)

    # --------------------------------------------------------------------------
    # Returns inverse of rotation matrix
    # Inversion of rotation matrix is just its transpose
    # --------------------------------------------------------------------------
    def invert(self):
        vect_x = self.vect_x
        vect_y = self.vect_y
        vect_z = self.vect_z

        self.vect_x = Vector3.from_vect([vect_x.vect[0], vect_y.vect[0], vect_z.vect[0]])
        self.vect_y = Vector3.from_vect([vect_x.vect[1], vect_y.vect[1], vect_z.vect[1]])
        self.vect_z = Vector3.from_vect([vect_x.vect[2], vect_y.vect[2], vect_z.vect[2]])

    # --------------------------------------------------------------------------
    # Convert from rotation matrix to euler angles
    # --------------------------------------------------------------------------
    def toEuler(self):
        if abs(self.vect_x.vect[2]) != 1:
            y = -1 * math.asin(self.vect_x.vect[2])
            x = math.atan2(self.vect_y.vect[2]/(math.cos(y)), self.vect_z.vect[2]/(math.cos(y)))
            z = math.atan2(self.vect_x.vect[1]/(math.cos(y)), self.vect_y.vect[1]/(math.cos(y)))
        else:
            z = 0
            if self.vect_x.vect[2] == -1:
                y = math.pi / 2
                x = z + atan2(self.vect_y.vect[0], self.vect_z.vect[0])
            else:
                y = - math.pi / 2
                x = - z + atan2(-self.vect_y.vect[0], -self.vect_z.vect[0])
        return Euler(x, y, z)
        
    #def toAxisAngle(self):
        
    #def toQuaternion(self):

################################################################################
# AxisAngle(axis, angle)
# AxisAngle takes an axis Vector3 and an angle
################################################################################
class AxisAngle:
    # --------------------------------------------------------------------------
    # Initialisation method
    # --------------------------------------------------------------------------
    def __init__(self, axis, angle):
        self.axis = axis
        self.angle = angle
    
    # --------------------------------------------------------------------------
    # Define test and print characteristics
    # --------------------------------------------------------------------------
    def __repr__(self):
        return "[axis: {}, angle: {}]".format(self.axis, self.angle)

    def __str__(self):
        return "[axis: {}, angle: {}]".format(self.axis, self.angle)

################################################################################
# AxisAngle(axis, angle)
# AxisAngle takes an axis Vector3 and an angle
################################################################################
class Quaternion:
    # --------------------------------------------------------------------------
    # Initialisation method
    # --------------------------------------------------------------------------
    def __init__(self, w, i, j, k):
        self.w = w
        self.i = i
        self.j = j
        self.k = k
    
    # --------------------------------------------------------------------------
    # Define test and print characteristics
    # --------------------------------------------------------------------------
    def __repr__(self):
        return "[w: {}, i: {}, j: {}, k: {}]".format(self.w, self.i, self.j, self.k)

    def __str__(self):
        return "[w: {}, i: {}, j: {}, k: {}]".format(self.w, self.i, self.j, self.k)