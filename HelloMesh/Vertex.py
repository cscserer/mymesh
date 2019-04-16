import HalfEdge
from Vector3D import *


class Vertex(object):
    """
    initialize the variables
    p the position
    out a out HalfEdge of all
    n the in/out degree
    index
    """
    def __init__(self, p=Vector3D(), out=None, n=0, index=0):
        self.p = p
        self.out = out
        self.n = n
        self.index = index

    def __repr__(self):
        return self.p.__repr__()

if __name__ == '__main__':
    v = Vertex(Vector3D(0,0,0))
    print(v)