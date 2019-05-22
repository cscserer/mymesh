"""
    store a mesh constructor.
    a mesh contains an array of Vertices Faces and HalfEdges.
"""
from Face import *
from HalfEdge import *
from Vertex import *
from Vector3D import *


class Mesh(object):
    def __init__(self):
        self.faces = []
        self.vertices = []
        self.edges = []

    def read_from_off(self, path):
        with open(path) as f:
            counter = 0
            h = 0
            n = 0
            m = 0
            for line in f:
                if counter == 0:
                    if line.split()[0] != 'OFF':
                        print('This is not an OFF file')
                        break
                elif counter == 1:
                    (n, m, mm) = map(int, line.split())
                elif counter < n + 2:
                    (x, y, z) = map(float, line.split())
                    self.vertices.append(Vertex(p=Vector3D(x, y, z), index=counter - 2))
                elif counter < n + m + 2:
                    indices = [int(x) for x in line.split()]
                    v = indices[0]
                    indices = indices[1:]
                    h = []
                    for i in range(v - 1):
                        h.append(self.find_edge(indices[i], indices[i+1]))
                    h.append(self.find_edge(indices[v - 1], indices[0]))
                    for i in range(v - 1):
                        h[i].nh = h[i + 1]
                        h[i + 1].ph = h[i]
                    h[v - 1].nh = h[0]
                    h[0].ph = h[v - 1]
                    face = Face(side=h[v - 1], n=v, index=len(self.faces))
                    self.faces.append(face)
                    for i in range(v):
                        h[i].polygon = face
                counter += 1
        return self

    def find_edge(self, i1, i2):
        """
        return the index of halfedge from vertex i1 to i2
        if there is no such halfedge, build 2 halfedges between i1 an i2
        :param i1: index of source vertex
        :param i2: index of target vertex
        :return:
        """
        v1 = self.vertices[i1]
        v2 = self.vertices[i2]
        h = v1.out
        while h:
            if h.target.index == i2:
                return h
            h = h.last
        index = len(self.edges)
        h1 = HalfEdge.HalfEdge(source=v1, target=v2, index=index, last=v1.out)
        h2 = HalfEdge.HalfEdge(source=v2, target=v1, index=index + 1, last=v2.out, th=h1)
        h1.th = h2
        v1.out = h1
        v2.out = h2
        v1.n += 1
        v2.n += 1
        self.edges.append(h1)
        self.edges.append(h2)
        return h1

    def write_off(self, name='test.off'):
        """
        writes the data out to an OFF file named fname
        :param name: the file name
        :return: no return
        """
        with open(name, 'w') as f:
            f.write('OFF\n')
            f.write('{} {} 0\n'.format(len(self.vertices), len(self.faces)))

            for v in self.vertices:
                f.write('{}\n'.format(v.p))
            for face in self.faces:
                temp = []
                f.write('{}'.format(face.n))
                e = face.side
                for i in range(face.n):
                    f.write(' {}'.format(e.target.index))
                    e = e.nh
                f.write('\n')

        print('OFF written to:', name)

    def set_face_normal(self):
        for face in self.faces:
            face.set_normal();


if __name__ == '__main__':
    aaa = Mesh.read_from_off(Mesh(), path = 'mesh/1.off')
    aaa.write_off()