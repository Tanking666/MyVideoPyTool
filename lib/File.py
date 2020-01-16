# -- coding: utf-8 --
import hashlib
import os


class File:
    def __init__(self, path):
        if os.path.isfile(path):
            self.path = path
            self.type = ''
            self.name = os.path.basename(path)
            self.exten = os.path.splitext(path)[1][1:]
            self.size = os.path.getsize(path)
            self.md5 = ''
        else:
            self.path = ''

    def get_md5(self):
        if self.md5 == '':
            md5_l = hashlib.md5()
            with open(self.path, mode="rb") as f:
                by = f.read()
                f.close()
            md5_l.update(by)
            self.md5 = md5_l.hexdigest()
        return self.md5

    def get_md55(self):
        if self.md5 == '':
            md5_l = hashlib.md5()
            with open(self.path, mode="rb") as f:
                by = f.read(1024 * 1024 * 5)
                f.close()
            md5_l.update(by)
            self.md5 = md5_l.hexdigest()
        return self.md5
