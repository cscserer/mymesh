from Vector3D import *
import HalfEdge


class Face(object):
    """
    initialize the variables
    side a side HalfEdge
    n the HalfEdge number
    index
    normal the normal Vector3D
    """
    def __init__(self, side=None, n=0, index=0, normal=Vector3D()):
        self.side = side
        self.n = n
        self.index = index
        self.normal = normal

    def set_normal(self):
        h = self.side
        self.normal = Vector3D()
        for i in range(self.n):
            self.normal += Vector3D.cross_product(h.nh.target.p - h.target.p, h.source.p - h.target.p)
            h = h.nh
        self.normal.normalize()

