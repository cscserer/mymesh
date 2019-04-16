"""
    deal with operators with system, build up files.
"""
import os


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
    set = MeshFile.read_all('/home/first/code/py')
    print(set)