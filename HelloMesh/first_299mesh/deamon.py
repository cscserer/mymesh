"""
use umap projection all the off
"""
import umap
from sklearn.datasets import load_digits
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import os
from FeatureRepo import *
from MeshFile import *
import time
import NH
cc = ['#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#46f0f0', '#f032e6', '#bcf60c', '#fabebe', '#008080', '#e6beff', '#9a6324', '#fffac8', '#800000', '#aaffc3', '#808000', '#ffd8b1', '#000075', '#808080']
category = {'cup': 7, 'ant': 3, 'human': 2, 'airplane': 6, 'armdino': 1, 'teddy': 9, 'glasses': 10,
            'fish': 12, 'fourleg': 14, 'octopus': 8, 'bird': 11, 'plier': 13, 'chair': 15, 'hand': 5, 'table': 4}
feature = ['agd', 'area', 'cf', 'geobase', 'mytanhgaussian', 'normalsangle', 'sdfval']


def retrieve_data(data, id, comb):
    input_data = []
    input_target = []
    target_names = set()
    input_file = []
    pos = 0
    for i in range(len(data.meshes)):
        kind_number = int(data.meshes[i].id.kind.split('_')[0])
        kind_char = data.meshes[i].id.kind.split('_')[1]
        if (id >> (kind_number - 1)) % 2 == 1:
            target_names.add(kind_char)
            input_data.append([])
            input_target.append(kind_char)
            input_file.append(data.meshes[i].id.path)
            for egg in comb:
                input_data[pos].extend(data.eggs[i][egg])
            pos += 1
    input_data = np.array(input_data)
    input_target = np.array(input_target)

    return(input_data, input_target, target_names, input_file)


class Result(object):
    def __init__(self, embedding, input_file, input_data, target, target_names, save_path, file_name, method, comb):
        self.x = embedding[:, 0]
        self.y = embedding[:, 1]
        self.input_data = input_data
        self.nh = NH.get_NH(self.x, self.y, target, k)
        self.mean_nh = self.nh.mean()
        self.target = target
        self.c = []
        self.nhc = []
        for i in range(len(target)):
            self.c.append(cc[category[target[i]]])
            self.nhc.append("#{}".format(hex(int(self.nh[i] * 255)).__str__()[2:] * 3))

        self.input_file = input_file
        self.target_names = target_names
        self.save_path = save_path
        self.file_name = file_name
        self.method = method
        self.png_path = ""
        self.npz_path = ""
        self.comb = comb

    def save(self):
        self.png_path = self.save_path + self.file_name + "_" + self.method + ".png"
        self.npz_path = self.save_path + self.file_name + "_" + self.method + ".npz"
        np.savez(self.npz_path, files=self.input_file, data=self.input_data, target=self.target,
                 x=self.x, y=self.y, nh=self.nh, c=self.c, nhc=self.nhc, comb=self.comb)
        for c in target_names:
            mask = input_target == c
            plt.scatter(self.x[mask], self.y[mask], label=c, c=cc[category[c]])
        plt.title("{}_{}_NH:{}".format(self.file_name, self.method, self.mean_nh))
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        plt.savefig(fname=self.png_path)
        plt.clf()

    def __eq__(self, other):
        return self.mean_nh == other.mean_nh

    def __lt__(self, other):
        return self.mean_nh < other.mean_nh


if __name__ == '__main__':
    test_mode = False
    path = '/home/first/code/data/seg_bench'
    order_path = '/home/first/code/data/seg_bench/results/order/'
    print("initialize data")
    data = FeatureRepo.init(path)
    data.load_all_eggs()
    print("initialization complete, total {} meshes".format(len(data.meshes)))

    while True:
        print(time.ctime())
        time.sleep(1)

        po = order_path + 'order.txt'
        pt = order_path + 'todo.txt'
        if os.path.exists(po):
            with open(po) as f:
                t = f.read()
                with open(pt, 'a') as ff:
                    ff.write(t)
                os.remove(po)
        if os.path.exists(pt):
            with open(pt) as f:
                k = 12  # k_nearest neighbor of NH
                for line in f:
                    args = line.split()
                    des_path = args[0]
                    method = args[2]
                    work = args[1].split('_')
                    id = int(work[0])
                    if method == "TOP":
                        maxi = 1 << len(feature)
                        ulist =[]
                        tlist = []
                        for i in range(1, maxi):
                            comb = []
                            file_name = id.__str__()
                            for j in range(len(feature)):
                                if 1 << j & i:
                                    comb.append(feature[j])
                                    file_name += "_" + feature[j]
                            input_data, input_target, target_names, input_file = retrieve_data(data, id, comb)
                            embedding = umap.UMAP().fit_transform(input_data)
                            ulist.append(Result(embedding=embedding, input_file=input_file, input_data=input_data, target=input_target,
                                                target_names=target_names, save_path=des_path, file_name=file_name, method="UMAP",
                                                comb =comb))
                            embedding = TSNE().fit_transform(input_data)
                            tlist.append(Result(embedding=embedding, input_file=input_file, input_data=input_data, target=input_target,
                                                target_names=target_names, save_path=des_path, file_name=file_name, method="TSNE",
                                                comb =comb))
                        ulist.sort(reverse=True)
                        tlist.sort(reverse=True)
                        store = dict()
                        for i in range(len(ulist)):
                            ulist[i].save()
                            tlist[i].save()
                            store["UMAP_{}".format(i)] = ulist[i].png_path
                            store["TSNE_{}".format(i)] = tlist[i].png_path
                        with open(des_path+args[1]+"_TOP" + '.txt','w') as f:
                            f.write(store.__str__())
                    else:
                        input_data, input_target, target_names, input_file = retrieve_data(data, id, work[1:])
                        if method == "UMAP":
                            embedding = umap.UMAP().fit_transform(input_data)
                        if method == "TSNE":
                            embedding = TSNE().fit_transform(input_data)
                        res = Result(embedding=embedding, input_file=input_file, input_data=input_data, target=input_target,
                                     target_names=target_names, save_path=des_path, file_name=args[1], method=method,
                                     comb =work[1:])
                        res.save()
                os.remove(pt)




