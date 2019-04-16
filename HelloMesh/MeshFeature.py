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
    def __init__(self, file=None, mesh=None, data=None, data_type=''):
        self.mesh = mesh
        self.id = file
        if data is None:
            data = np.array([])
        self.data = data
        self.data_type = data_type
        self.hist = np.array([])

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

    def feature_face_normal_length(self, min_value, max_value, number = 10):
        feature = np.zeros(10)
        interval = (max_value - min_value) / number
        for face in self.mesh.faces:
            temp = (face.normal.length - min_value) // interval
            print(face.normal.length - min_value ,interval , temp)
            temp = max(min(temp, number - 1), 0)
            print(temp)
            feature[temp] += 1
        feature = feature / sum(feature)
        return feature


if __name__ == '__main__':
    ids = MeshFile.read_all('/home/first/code/data/seg_bench/8_octopus')
    Meshes = []
    for i in ids:
        m = MeshFeature(file=i)
        m.get_feature('area')
        m.save_feature()