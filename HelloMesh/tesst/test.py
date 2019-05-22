"""
try some python function
"""
import numpy as np

import matplotlib.pyplot as plt
import os



print(os.getcwd())
a = "1   3 432  5 3.npz"
print(a[:-4])
print(a.split())
print(len(a.split()))
mask = list(range(10))
print(mask)
print(plt.style.available)

print(1<<16)


a = np.array([[1,3,4],[1,3,4]])

print(a.shape[0])
print(a.size)

a = dict()
a['1342'] = "hgjklkjhl"
a['42342']= "dasd"
print(a)
s = a.__str__()
b = eval(s)

print(s,b)
for i in range(1000):
    s += i.__str__()
f = open('fasd.txt', 'w')
f.write(s)
f.close()

f = open('fasd.txt')
t = f.read()
print(t)
print(t.__eq__(s))

class TempC(object):
    def __init__(self,x ,y):
        self.x = x;
        self.y = y;

    def __eq__(self, other):
        return self.y == other.y
    def __lt__(self, other):
        return self.y < other.y
    def __repr__(self):
        return self.x.__str__() + self.y.__str__()


def takex(elem):
    return elem.y

s = ".//order/"
if not os.path.exists(s):
    os.makedirs(s)
x = [1,2,3,4,5,6,7,8,9]
y = [4,7,2,4,6,8,2,5,7]
a = []
for i in range(len(x)):
    temp = TempC(x[i],y[i])
    a.append(temp)
print(a)
a.sort()
print(a)


print ("#{}".format(hex(int(255)).__str__()[2:] * 3))