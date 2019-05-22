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
cc = ['#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#46f0f0', '#f032e6', '#bcf60c', '#fabebe', '#008080', '#e6beff', '#9a6324', '#fffac8', '#800000', '#aaffc3', '#808000', '#ffd8b1', '#000075', '#808080']


if __name__ == '__main__':
    test_mode = False
    path = '/home/first/code/data/seg_bench'
    # path = '/home/first/code/data/seg_bench/1_armdino/desc'
    data = None
    while True:
        input_str = input("Please input:").split('*')
        for str in input_str:
            if len(str) == 0:
                continue
            if str == "-e" or str == "-exit":
                exit()
            elif str == "-u" or str == '-umap' or str == "u":
                umap_data = np.array(data.data)
                umap_target = np.array(data.target)
                embedding = umap.UMAP().fit_transform(umap_data)
                x = embedding[:, 0]
                y = embedding[:, 1]
                counter = 0
                target_color = {}
                for c in data.target_names:
                    target_color[c] = cc[counter]
                    counter += 1
                for c in data.target_names:
                    mask = umap_target == c
                    plt.scatter(x[mask], y[mask],label = c, c=target_color[c])
                plt.legend(loc='center left',bbox_to_anchor=(1, 0.5))
                plt.show()
                continue
            elif str=="-t" or str == "-tsne" or str == "t":
                tsne_data = np.array(data.data)
                tsne_target = np.array(data.target)
                embedding = TSNE().fit_transform(tsne_data)
                x = embedding[:, 0]
                y = embedding[:, 1]
                counter = 0
                target_color = {}
                for c in data.target_names:
                    target_color[c] = cc[counter]
                    counter += 1
                for c in data.target_names:
                    mask = tsne_target == c
                    plt.scatter(x[mask], y[mask], label=c, c=target_color[c])
                plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
                plt.show()
                continue
            elif str == "-c" or str == "-clean" or str == "c":
                print("clean features")
                if not (data is None):
                    data.clean()
                    print("cleaning complete")
                else:
                    print(" there is no data here")
                continue
            elif (str == "-ca" or str == "-clear all"):
                print("clean all data")
                if not (data is None):
                    data.clean_all()
                    data = None
                    print("cleaning complete")
                else:
                    print("there is no data here")
                continue
            elif str == "-i" or str == "-init" or str == "i":
                print("initialize data")
                data = FeatureRepo.init(path)
                print("initialization complete, total {} meshes".format(len(data.meshes)))
                continue
            elif str[:2] == "-p":
                print("set path")
                temp = str[2:].strip()
                path = temp
                if not (data is None):
                    data.set_path(path)
                print('set path to {}'.format(path))
            elif str[0] == '-':
                print('there is no such command')
            else:
                input_type = str.split()
                for type in input_type:
                    if type[0] == '-':
                        print("type should not start with -")
                        continue
                    print("add feature type {}".format(type))
                    if not (data is None):
                        temp = data.get_feature(type)
                        if temp:
                            print("add successful")
                        else:
                            print("add None")
                    else:
                        print("there is no data here")
                    continue

    # digits = load_digits()
    # print((digits))
    # print(digits.data.shape)
    # print(digits.target.size)
    # print(digits.target)
    # embedding = umap.UMAP().fit_transform(digits.data)
    #
    # print(type(embedding))
    # x = embedding[:, 0]
    # y = embedding[:, 1]
    #
    # for c in digits.target_names:
    #     mask = digits.target == c
    #     print(x[mask].shape, y[mask].shape, digits.target[mask].shape)
    #     plt.scatter(x[mask], y[mask],label = c)
    # plt.legend(loc='center left',bbox_to_anchor=(1, 0.5))
    # plt.show()
