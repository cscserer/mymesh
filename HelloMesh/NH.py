import numpy as np
import heapq


def count_NH_path():
    return

def get_NH(x, y, t, k):
    n = x.shape[0]
    nh = []
    for i in range(n):
        heap = []
        for j in range(n):
            dis = (x[j] - x[i]) ** 2 + (y[j] - y[i]) ** 2
            if t[i] == t[j]:
                diff = 0
            else:
                diff = 1
            item = (dis, diff, j)
            heap.append(item)
        heapq.heapify(heap)
        res = (heapq.nsmallest(k, heap))
        hit = 0
        for j in res:
            hit += 1 - j[1]
        nh.append(hit)
    return np.array(nh) / k

if __name__ == '__main__':
    x = np.array([5,1,2,3,4,6,7,8,9])
    y = np.array([0,0,0,0,0,0,0,0,0])
    t = np.array([1,2,3,4,5,1,2,4,5])
    k = 6
    print(get_NH(x,y,t,k))



