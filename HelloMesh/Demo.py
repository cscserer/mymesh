"""
use umap projection all the off
"""
import umap
from sklearn.datasets import load_digits
import matplotlib.pyplot as plt
import os
from FeatureRepo import *
from MeshFile import *


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
                break
            elif str == "-u" or str == '-umap' or str == "u":
                umap_data = np.array(data.data)
                umap_target = np.array(data.target)
                embedding = umap.UMAP().fit_transform(umap_data)
                x = embedding[:, 0]
                y = embedding[:, 1]
                for c in data.target_names:
                    mask = umap_target == c
                    plt.scatter(x[mask], y[mask],label = c)
                plt.legend(loc='center left',bbox_to_anchor=(1, 0.5))
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
