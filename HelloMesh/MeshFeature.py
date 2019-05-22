"""
get mesh ready to be used

mesh the structure of the mesh, record as Mesh
data the feature
data_type a string to describe the feature
id the MeshFile
"""
from Mesh import *
from MeshFile import *
from Vector3D import *
import math
import os


class MeshFeature(object):
    def __init__(self, file=None, mesh=None, data=None, data_type=''):
        self.mesh = mesh
        self.id = file
        if data is None:
            data = np.array([])
        self.data = data
        self.data_type = data_type
        self.hist = np.array([])

        self.django_keys = {}

    def clean(self):
        self.data = np.array([])
        self.data_type = ''

    def get_feature(self, type, new_first=True):
        aim = self.id.dir + "/desc/{name}_{type}_new.{suffix}".format(name=self.id.name, type=type, suffix='txt')
        if not os.path.exists(aim):
            aim = self.id.dir + "/desc/{name}_{type}.{suffix}".format(name=self.id.name, type=type, suffix='txt')
        if os.path.exists(aim):
            with open(aim) as f:
                list = []
                for line in f:
                    list.append(float(line))
                self.data = np.array(list)
                self.data_type = type
        else:
            return False
        return True

    def get_feature_path(self, type, new_first=True):
        aim = self.id.dir + "/desc/{name}_{type}_new.{suffix}".format(name=self.id.name, type=type, suffix='txt')
        if not os.path.exists(aim):
            aim = self.id.dir + "/desc/{name}_{type}.{suffix}".format(name=self.id.name, type=type, suffix='txt')
        if os.path.exists(aim):
            self.django_keys[type] = aim

    def get_django_statistics(self):
        self.load_mesh()
        self.django_keys['total_vertices'] = len(self.mesh.vertices)
        self.django_keys['total_faces'] = len(self.mesh.faces)
        self.get_feature('area')
        self.django_keys['min_area'] = self.data.min()
        self.django_keys['total_area'] = self.data.sum()
        self.django_keys['max_area'] = self.data.max()
        self.django_keys['mean_area'] = self.data.mean()
        self.django_keys['std_area'] = self.data.std()
        self.django_keys['var_area'] = self.data.var()


    def save_feature(self, update=True):
        aim = self.id.dir + "/desc/{name}_{type}.{suffix}".format(name=self.id.name, type=self.data_type, suffix='txt')
        if os.path.exists(aim):
            aim = self.id.dir + "/desc/{name}_{type}_new.{suffix}".format(name=self.id.name, type=self.data_type, suffix='txt')
        aim_dir = self.id.dir + '/desc/'
        if not os.path.exists(aim_dir):
            os.mkdir(aim_dir)
        if os.path.exists(aim):
            if update:
                os.remove(aim)
        np.savetxt(aim, self.data)

    def load_mesh(self):
        self.mesh = Mesh().read_from_off(path=self.id.path)
        return self

    def get_face_normal(self):
        """
        make every mesh count its faces' normal vector
        :return:
        """
        if self.mesh is None:
            self.load_mesh()
        self.mesh.set_face_normal()

    def feature_gaussian_curvature(self):
        if self.mesh is None:
            self.load_mesh()
        list = []
        for v in self.mesh.vertices:
            edge = v.out
            sum_angle = 0
            sum_area = 0

            p = v.p
            for i in range(v.n):
                # print(v.index, edge.target.index, edge.ph.th.target.index, sum_area)
                # print(edge.polygon.index, edge.ph.th.polygon.index)
                p1 = edge.target.p
                edge = edge.ph.th
                p2 = edge.target.p
                v1 = p2 - p
                v2 = p1 - p

                v2.normalize()
                v1.normalize()
                sum_area += Vector3D.cross_product(v1, v2).length / 2.0

                # print(v1, v2, Vector3D.dot_product(v1, v2), np.arccos(Vector3D.dot_product(v1, v2)), sum_area)
                sum_angle += math.acos(Vector3D.dot_product(v1, v2))

            gaussian = (2*math.pi - sum_angle) * 4 / sum_area

            list.append(math.tanh(gaussian))

        self.data = np.array(list)
        self.data_type = 'mytanhgaussian'

if __name__ == '__main__':
    ids = MeshFile.read_all('/home/first/code/data/seg_bench/')
    # ids = MeshFile.read_all('/home/first/code/py/HelloMesh')
    Meshes = []
    for i in ids:
        print(i)
        m = MeshFeature(file=i)
        m.feature_gaussian_curvature()
        m.save_feature()