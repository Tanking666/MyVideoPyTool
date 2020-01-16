# -- coding: utf-8 --
import os

from lib import File


class Dir:
    def __init__(self, path):
        if os.path.isdir(path):
            self.path = path
            self.name = os.path.basename(self.path)

            self.listData = []
            for x in os.listdir(self.path):
                self.listData.append(self.path + '/' + x)

            self.listDirPath = [x for x in self.listData if os.path.isdir(x)]
            self.listFile = [File.File(x) for x in self.listData if os.path.isfile(x)]
        else:
            self.listDirPath = []
            self.listFile = []
            self.path = ''
            self.name = ''

    def rename(self, new_name):
        if not str(new_name).startswith("[") and self.listDirPath == []:
            new_name = "[" + new_name
        if not str(new_name).endswith("]") and self.listDirPath == []:
            new_name = new_name + "]"
        if self.path != '' and self.name != new_name and self.listDirPath == []:
            print(self.path + "=>" + os.path.dirname(self.path) + '/' + new_name)
            os.rename(self.path, os.path.dirname(self.path) + '/' + new_name)
