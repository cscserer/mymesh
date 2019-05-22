"""
    deal with operators with system, build up files.
"""
import os

category = {'cup': 7, 'ant': 3, 'human': 2, 'airplane': 6, 'armdino': 1, 'teddy': 9, 'glasses': 10,
            'fish': 12, 'fourleg': 14, 'octopus': 8, 'bird': 11, 'plier': 13, 'chair': 15, 'hand': 5, 'table': 4}

class MeshFile(object):
    """
    path the system path
    kind what is the mesh
    suffix which file type is the mesh saved
    name the name
    """
    def __init__(self, path):
        s = path.split('/')
        self.dir = os.path.abspath("/".join(s[:-1]))
        kind = s[-2]
        s = s[-1].split('.')
        suffix = s[1].upper()
        name = s[0]
        self.path = os.path.abspath(path)
        self.kind = kind
        self.suffix = suffix
        self.name = name


    def __repr__(self):
        return 'name:{} path:{} dir:{} kind:{} suffix:{}'.format(self.name, self.path, self.dir, self.kind, self.suffix)

    @staticmethod
    def read_all(path, suffix=None):
        if suffix is None:
            suffix = {'OFF'}
        else:
            suffix = {suffix}
        list = []
        list.extend([path + '/' + x for x in os.listdir(path)])
        out = []
        for aim in list:
            if os.path.isdir(aim):
                list.extend(aim + '/' + x for x in os.listdir(aim))
            else:
                if aim.split('.')[-1].upper() in suffix:
                    out.append(MeshFile(aim))
        return out
if __name__ == '__main__':
    dat = MeshFile.read_all('/home/first/code/data/seg_bench')
    for i in dat:
        print('"{}",'.format(i.path), end="")
        d = '/home/first/code/data/uni_299data/{}'.format(i.kind)
        if not (os.path.exists(d)):
            os.mkdir(d)
    print()
    print(len(dat))
    for i in dat:
        print('"/home/first/code/data/uni_299data/{}/{}.off",'.format(i.kind, i.name), end="")
    print()
    k = set({})
    for i in dat:
        k.add(i.kind)
    print(k)



