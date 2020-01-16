# coding=utf-8
import hashlib
import os

from lib import Video
from lib.util import video_util, z7_util


class FileItem:

    def __init__(self, path):
        if not str.endswith(path, "/"):
            path = path + "/"
        if os.path.isdir(path):
            self.path = path
            self.pathName = os.path.basename(self.path[:-1])
            self.listData = os.listdir(self.path)
            self.listFilePath = [path + x for x in self.listData if os.path.isfile(path + x)]
            self.listFile = [x for x in self.listData if os.path.isfile(path + x)]
            self.listDirPath = [path + x for x in self.listData if os.path.isdir(path + x)]
            self.is_packing()
            self.packingFlag = self.is_packing()
        else:
            print(path + "is not DIR")
            self.path = ''

    def is_packing(self):
        return os.path.isfile(self.path + '/$$myflag')

    def get7z01(self):
        for x in self.listFilePath:
            if str(x).endswith(".7z.001"):
                return x
            elif str(x).endswith(".7z"):
                return x
        return ''

    def set_packing(self):
        f = open(self.path + "$$myflag", "w")
        f.close()
        self.packingFlag = True

    def remove_packing(self):
        if self.is_packing():
            os.remove(self.path + '$$myflag')
        self.packingFlag = False

    def clean_pack(self):
        for x in self.listFilePath:
            if len(x) > 7:
                if x[-7:-3] == '.7z.':
                    os.remove(x)

    def un_pack(self, to_dir):
        if not self.get7z01() == '':
            z7_util.z7Tools().unPack(self.get7z01(), to_dir)
            self.remove_packing()
            if not self.is_packing():
                self.clean_pack()

    def getmd5(self, to_dir):
        md5_l = hashlib.md5()
        ret = ''
        for x in self.listFile:
            if not x == 'md5.txt':
                with open(self.path + x, mode="rb") as f:
                    by = f.read()
                md5_l.update(by)
                ret = ret + x + '\t\t' + md5_l.hexdigest() + '\n'
                print(x + '\t\t' + md5_l.hexdigest())
        f = open(to_dir + 'md5.txt', 'w')
        f.write(ret)
        f.close()

    def save_or_update(self):
        for x in self.listFilePath:
            v = Video.Video(x)
            v.save_or_update()

    def save_or_update_one(self, path):
        print(path)
        v = Video.Video(path)
        v.save_or_update()




if __name__ == '__main__':
    f1 = FileItem(r"X:\Video\!泡面\[copihan][01-07][X264_AAC][640×360][10bit]")
    f1.un_pack(r"X:\Video\!泡面\[2017][野良和皇女和流浪猫之心][Nora to Oujo to Noraneko Heart][720P][GB][MP4] - 副本")
