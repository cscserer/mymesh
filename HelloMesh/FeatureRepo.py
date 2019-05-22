"""
deal with the feature for picking up and storing
"""
import os
from MeshFile import *
from MeshFeature import *


class FeatureRepo(object):
    """
    path indicate where to find stored feature

    eggs used for store the features and features names in a list of dictionary
    usage:
     setpath, load_mesh, get_data, get histogram
    """
    def __init__(self):
        self.path = os.curdir
        self.meshes = []
        self.data = []
        self.target = []
        self.target_names = set()
        self.type = ""
        #  eggs used for store the features and features names in a list of dictionary
        self.eggs = []
        self.egg_names = set()
        # self.types = ['x', 'y', 'z',
        #          'agd', 'area', 'cf', 'mytanhgaussian', 'geobase',
        #          'normalsangle', 'sdfval']
        self.types = ['agd', 'area', 'cf', 'mytanhgaussian', 'geobase',
                 'normalsangle', 'sdfval']

    def clean(self):
        self.data = []
        self.type = ""

    def clean_all(self):
        self.clean()
        self.target = []
        self.target_names = set()
        self.meshes = []

    def set_path(self, path):
        self.path = path

    def load_mesh(self):
        mesh_ids = MeshFile.read_all(self.path)
        for m in mesh_ids:
            feature = MeshFeature(file=m)
            self.meshes.append(feature)
            self.target.append(m.kind)
            self.target_names.add(m.kind)

    def get_data(self, type):
        for m in self.meshes:
            m.clean()
            temp = m.get_feature(type)
            if not temp:
                print("mesh {}, does not have feature {}".format(m.id, type))

    def save_feature(self, type):
        for m in self.meshes:
            m.save_feature(type)
        return

    def get_histogram(self, number=10):
        if len(self.meshes):
            min_value = None
            max_value = None
            egg_name = None
            for m in self.meshes:
                if m.data.size > 0:
                    if min_value is None:
                        min_value = m.data.min()
                        max_value = m.data.max()
                    else:
                        if egg_name is None:
                            egg_name = m.data_type
                        min_value = min(min_value, m.data.min())
                        max_value = max(max_value, m.data.max())
            if min_value is None:
                print('all meshes do not have such feature')
                return False
            self.egg_names.add(egg_name)
            interval = (max_value - min_value) / number
            for j in range(len(self.meshes)):
                m = self.meshes[j]
                hist = np.zeros(number)
                if m.data.size > 0:
                    for i in m.data:
                        temp = int((i - min_value) // interval)
                        temp = min(temp, number - 1)
                        hist[temp] += 1
                    hist = hist / sum(hist)
                m.hist = hist
                if len(self.data) <= j:
                    self.eggs.append({})
                    self.data.append(m.hist.tolist())
                else:
                    self.data[j].extend(m.hist.tolist())
                self.eggs[j][egg_name] = m.hist.tolist()
            return True

    def get_feature(self, type):
        self.get_data(type)
        temp = self.get_histogram()
        if temp:
            self.type += type
        return temp

    @staticmethod
    def init(path=os.curdir):
        """
        setpath, load_mesh
        :param path: the repository of meshes
        :return:
        """
        data = FeatureRepo()
        data.set_path(path)
        data.load_mesh()
        return data

    @staticmethod
    def create_feature_position_x(path=os.curdir):
        data = FeatureRepo.init(path)
        for m in data.meshes:
            m.data_type = 'x'
            m.load_mesh()
            list = []
            for v in m.mesh.vertices:
                list.append(v.p.x)
            m.data = np.array(list)
            m.save_feature()

    @staticmethod
    def create_feature_position_y(path=os.curdir):
        data = FeatureRepo.init(path)
        for m in data.meshes:
            m.data_type = 'y'
            m.load_mesh()
            list = []
            for v in m.mesh.vertices:
                list.append(v.p.y)
            m.data = np.array(list)
            m.save_feature()

    @staticmethod
    def create_feature_position_z(path=os.curdir):
        data = FeatureRepo.init(path)
        for m in data.meshes:
            m.data_type = 'z'
            m.load_mesh()
            list = []
            for v in m.mesh.vertices:
                list.append(v.p.z)
            m.data = np.array(list)
            m.save_feature()

    def load_all_eggs(self):
        """
            x,y,z the positions of vertices
            agd average geodesic distance
            cf  conformal factors
            geobase distance to the bottom
            sdfval shape diameter function   average thichness

        :return:
        """
        for t in self.types:
            self.get_feature(t)

    def load_for_django_model(self):
        mesh_ids = MeshFile.read_all(self.path)
        for m in mesh_ids:
            feature = MeshFeature(file=m)
            self.meshes.append(feature)
        for m in self.meshes:
            for t in self.types:
                m.get_feature_path(t)
            m.get_django_statistics()
            m.django_keys['s_version'] = 0
            m.django_keys['m_version'] = 0
            m.django_keys['f_version'] = 0


if __name__ == "__main__":
    print("running FeatureRepo")
    # path = os.curdir
    path = '/home/first/code/data/seg_bench/'
    data = FeatureRepo()
    data.set_path(path)

    # data.load_mesh()
    # data.load_all_eggs()
    # print(data.eggs)


    # data.get_data('area')
    # data.get_histogram()
    # data.save_feature('area')
