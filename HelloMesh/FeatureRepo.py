"""
deal with the feature for picking up and storing
"""
import os
from MeshFile import *
from MeshFeature import *

class FeatureRepo(object):
    """
    repo_path indicate where to find stored feature
    usage:
     setpath, load_mesh, get_data, get histogram
    """
    def __init__(self):
        self.path = os.curdir
        self.meshes = []

    def set_path(self, path):
        self.path = path

    def load_mesh(self):
        mesh_ids = MeshFile.read_all(self.path)
        for m in mesh_ids:
            feature = MeshFeature(file=m)
            self.meshes.append(feature)

    def get_data(self, type):
        for m in self.meshes:
            temp = m.get_feature(type)
            if not temp:
                print("mesh {}, does not have feature {}".format(m.file, type))

    def save_feature(self, type):
        for m in self.meshes:
            m.save_feature(type)
        return

    def get_histogram(self, number=10):
        if len(self.meshes):
            min_value = self.meshes[0].data[0]
            max_value = min_value
            for m in self.meshes:
                min_value = min(min_value, m.data.min())
                max_value = max(max_value, m.data.max())
            interval = (max_value - min_value) / number
            for m in self.meshes:
                hist = np.zeros(number)
                for i in m.data:
                    temp = int((i - min_value) // interval)
                    temp = min(temp, number - 1)
                    hist[temp] += 1
                hist = hist / sum(hist)
                m.hist = hist

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

    def get_feature(self, type):
        self.get_data(type)
        self.get_histogram()


if __name__ == "__main__":
    path = os.curdir
    path = '/home/first/code/data/seg_bench/8_octopus'
    data = FeatureRepo()
    data.set_path(path)
    data.load_mesh()
    data.get_data('area')
    data.get_histogram()
    data.save_feature('area')
