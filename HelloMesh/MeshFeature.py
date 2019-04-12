"""
get mesh ready to be used

mesh the structure of the mesh, record as Mesh
data the feature
data_type a string to describe the feature
id the MeshFile
"""
from Mesh import *
from MeshFile import *
import os


class MeshFeature(object):
    def __init__(self, mesh=None, data=None, data_type='', id = None):
        self.mesh = mesh
        self.id = id
        if data is None:
            data = []
        self.data = data
        self.data_type = data_type

    def clear(self):
        self.data = []
        self.data_type = ''

    def get_feature(self, f):
        if f == 'face_normal':
            self.get_face_normal()

    def load_mesh(self):
        self.mesh = Mesh().read_from_off(path=self.id.path)
        return self

    def get_face_normal(self):
        if self.mesh is None:
            self.load_mesh()
        self.mesh.set_face_normal()

if __name__ == '__main__':
    ids = MeshFile.read_all(os.curdir)
    Meshes = []
    for i in ids:
        m = MeshFeature(id=i)
        m.load_mesh()
        for v in m.mesh.vertices:
            print(v.p)
        Meshes.append(m)

    for mesh in Meshes:
        mesh.get_face_normal()

        for f in mesh.mesh.faces:
            print(f.normal)