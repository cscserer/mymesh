"""
try different combinations
"""
import umap
import matplotlib.pyplot as plt
import os
from FeatureRepo import *
from MeshFile import *

y = []
def dfs(n):
    if n > 0:
        if sum(mask) > 0:
            aim_dir = os.path.abspath(os.curdir) + "/DemoCombo/"
            if not os.path.exists(aim_dir):
                os.mkdir(aim_dir)
            file_name = aim_dir + "i*"
            for j in range(n):
                if (mask[j]):
                    file_name += data.types[j] + "*"
            file_name += "u"
            x = []
            for i in range(len(data.meshes)):
                x.append([])
                for j in range(n):
                    if (mask[j]):
                        x[i].extend(data.eggs[i][data.types[j]])

            umap_data = np.array(x)
            umap_target = np.array(y).squeeze()
            embedding = umap.UMAP().fit_transform(umap_data)
            xx = embedding[:, 0]
            yy = embedding[:, 1]
            print(len(xx), len(yy))
            for c in target_names:
                m = umap_target == c
                print(c, m , yy)
                plt.scatter(xx[m], yy[m], label=c)
            aim  = file_name + ".npz"
            np.savez(data=umap_data, target=umap_target, ux=xx, uy=yy)
            plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
            plt.savefig(aim + ".jpg")
    if n == maxdepth:
        return
    mask[n] = 1
    dfs(n + 1)
    mask[n] = 0
    dfs(n + 1)
maxdepth = 0
mask = []

target_names = dat()
if __name__ == '__main__':
    test_mode = False
    path = '/home/first/code/data/seg_bench/1_armdino'
    # path = '/home/first/code/data/seg_bench/1_armdino/desc'
    data = None
    data = FeatureRepo()
    data.set_path(path)
    data.load_mesh()
    # data.load_all_eggs()

    maxdepth = len(data.types)
    mask = np.zeros(maxdepth)
    y = np.array(data.target).reshape(len(data.target), 1)
    target_names = data.target_names
    dfs(0)
