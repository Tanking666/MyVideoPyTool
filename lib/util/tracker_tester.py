# -- coding: utf-8 --
import os

tracker_list = []

# -*- coding: utf-8 -*-

import subprocess
import re


def get_tracker_list():
    global tracker_list
    with open("../../tracker.txt", "r", encoding="utf-8") as f:
        txtlist = f.readlines()
        if len(txtlist) == 1:
            tracker_list = txtlist[0].split(",")
        elif len(txtlist) > 1:
            tracker_list = txtlist


def write_to_tracker_list(tm):
    global tracker_list
    with open("../../RealTrackerList.txt", "w", encoding="utf-8") as f:
        for x in tm:
            f.write(x)


def mapper():
    t_list = tracker_list
    tm = []
    # 过滤ipv6
    for x in t_list:
        if '[' in x:
            t_list.remove(x)
    for x in t_list:
        if str(x).endswith('\n'):
            tm.append(x[:-1] + '\t' + get_aurl(x) + '\n')
        else:
            tm.append(x + '\t' + get_aurl(x) + '\n')
    return tm


def get_aurl(url):
    res = str(url).replace("http://", '')
    res = res.replace("udp://", '')
    res = res.replace("https://", '')
    res = res.replace("wss://", '')
    if ":" in res:
        res = res[:res.index(':')]
    elif "/" in res:
        res = res[:res.index('/')]
    return res


if __name__ == '__main__':
    get_tracker_list()
    write_to_tracker_list(mapper())
    # write_to_tracker_list()
