# -- coding: utf-8 --

import os
import subprocess

Z7_PATH = '"C:\\Program Files\\7-Zip\\7z.exe"'
ROOT = os.path.abspath(os.curdir)
T_ROOT = ROOT
# T_ROOT = 'D:\\Temp'
print("\n\nROOT:" + ROOT)

all_list = os.listdir(ROOT)

all_dir_list = list()
for x in all_list:
    this_dir = ROOT + '\\' + x
    if os.path.isdir(this_dir):
        all_dir_list.append(x)
all_dir_list.remove('.idea')


def fun1():
    for i in all_dir_list:
        del_sw = ''
        this_dir = ROOT + '\\' + i
        new_dir = T_ROOT + '\\' + i
        if not os.path.isdir(new_dir):
            os.mkdir(new_dir)
        if T_ROOT == ROOT:
            del_sw = '-sdel'
        cmd = Z7_PATH + r' a -t7z "' + new_dir + '\\' + i + '.7z" "' + this_dir + '\\*" -mx=0 -r -pkxy123 -v1g ' + del_sw
        ps=subprocess.Popen(cmd)
        ps.wait()


if __name__ == '__main__':
    fun1()
