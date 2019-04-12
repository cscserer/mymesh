import Vertex


class HalfEdge(object):
    """
    initialize the variables
    target the target Vertex
    source the source Vertex
    nh the next HalfEdge
    ph the previous HalfEdge
    th the twin HalfEdge
    last the last half have the same source HalfEdge
    polygon the belonging Face
    index the index number
    """

    def __init__(self, target=None, source=None, nh=None, ph=None, th=None, polygon=None, last=None, index=0):
        self.target = target
        self.source = source
        self.nh = nh
        self.ph = ph
        self.th = th
        self.last = last
        self.polygon = polygon
        self.index = index

    def __repr__(self):
        return '{} --> {}'.format(self.source.p, self.target.p)

    def is_boundary(self):
        return self.polygon is None or self.th.polygon is None