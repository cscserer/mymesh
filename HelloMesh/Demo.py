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
    while True:
        data = None
        str = input("Please input:")
        print(str)
        if (str == "-e" or str == "-exit"):
            break
        if (str == "-c" or str == "-clear"):
            if not (data is None):
                break
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
