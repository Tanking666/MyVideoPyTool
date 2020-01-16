# coding=utf-8
import os
import subprocess


class z7Tools():
    def __init__(self):
        self.Z7_PATH = '"C:\\Program Files\\7-Zip\\7z.exe"'
        self.password = '-pkxy123'

    def pack(self, dataDir, targetDir, del_sw):
        if del_sw:
            del_sw = '-sdel'
        else:
            del_sw = ''
        z7name = os.path.basename(dataDir) + '.7z'
        cmd = self.Z7_PATH + r' a -t7z "' + targetDir + '\\' + z7name + '" "' + dataDir + '\\*" -mx=0 -r ' + self.password + ' -v1g ' + del_sw
        ps = subprocess.Popen(cmd)
        ps.wait()

    def unPack(self, z7pack, tagetDir):
        cmd = self.Z7_PATH + r' x "' + z7pack + '" -aos ' + self.password + ' -o"' + tagetDir + '" '
        ps = subprocess.Popen(cmd)
        ps.wait()


if __name__ == '__main__':
    z7 = z7Tools()
    z7.unPack(
        r"X:\Video\TV\[1979][凡尔赛玫瑰 Rose of Versailles][BDRIP][960X720][X264-10bit_AAC]\[异域-11番小队][凡尔赛玫瑰 Rose of Versailles][BDRIP][960X720][X264-10bit_AAC].7z.001",
        r"X:\Video\TV\[1979][凡尔赛玫瑰 Rose of Versailles][BDRIP][960X720][X264-10bit_AAC]\新建文件夹")
