"""
record a 3d position with x y z.
"""
import numpy as np


class Vector3D(object):
    def __init__(self, x=0., y=0., z=0.):
        self.data = np.array([x, y, z])

    def __repr__(self):
        return '{:6f} {:6f} {:6f}'.format(self.x, self.y, self.z)

    def __add__(self, other):
        out = Vector3D()
        out.data = self.data + other.data
        return out

    def __sub__(self, other):
        out = Vector3D()
        out.data = self.data - other.data
        return out

    @property
    def x(self):
        return self.data[0]

    @x.setter
    def x(self, value):
        self.data[0] = value

    @property
    def y(self):
        return self.data[1]

    @y.setter
    def y(self, value):
        self.data[1] = value

    @property
    def z(self):
        return self.data[2]

    @z.setter
    def z(self, value):
        self.data[2] = value

    @staticmethod
    def cross_product(v1, v2):
        c = np.cross(v1.data, v2.data)
        return Vector3D(c[0], c[1], c[2])

    def length(self):
        return sum(x**2 for x in self.data)

    def normalize(self):
        length = self.length()
        if length:
            self.data = self.data / length


if __name__ == '__main__':
    v1 = Vector3D(-6.4, -11.2, -7.2)
    v2 = Vector3D(-8, 16, 12)
    print(Vector3D.cross_product(v1, v2))