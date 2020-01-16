# coding=utf-8

import os
import threading

from core import fileItem

# T_ROOT = 'D:\\Temp'
from lib.Dir import Dir
from lib.File import File
from lib.Video import Video
from lib.util import mysql_util, ffmpeg_util

all_file = []
all_dir = []
mysql = mysql_util.MysqlUtil()


def get_all_file(Root):
    f = Dir(Root)
    try:
        all_file.extend(f.listFile)
        all_dir.extend(f.listDirPath)
    except BaseException:
        pass
    for x in f.listDirPath:
        get_all_file(x)


def ext(Root):
    f = fileItem.FileItem(Root)
    f.un_pack(f.path)
    for x in f.listDirPath:
        ext(x)


def getmd5(Root):
    f = fileItem.FileItem(Root)
    f.getmd5(f.path)
    for x in f.listDirPath:
        getmd5(x)


def save_to_db(file_list):
    i = 0
    for file in file_list:
        Video(file.path).save_or_update()
    mysql.execute("UPDATE video v set v.rate20 = v.size/1024/1024*60*20/v.len where v.rate20 is null")
    print(str(len(file_list)) + ':ALL_DONE')


def fix(Root):
    get_all_file(Root)
    for x in all_file:
        try:
            print(x.path + "==>" + os.path.dirname(x.path) + '/' + mysql_util.get_name_bysize_pname(
                os.path.dirname(x.path), x.size))
            if (x.path != os.path.dirname(x.path) + '/' + mysql_util.get_name_bysize_pname(os.path.dirname(x.path),
                                                                                           x.size)):
                os.rename(x.path,
                          os.path.dirname(x.path) + '/' + mysql_util.get_name_bysize_pname(os.path.dirname(x.path),
                                                                                           x.size))
        except BaseException:
            print("ERROR:" + x.path)


def save_to_db_t(Root, t):
    mysql_util.refrash_data()
    t = int(t)
    get_all_file(Root)
    print("ALL_FILE:" + str(len(all_file)))
    t_list = list()
    for i in range(t):
        t_list.append([])

    for x in range(len(all_file)):
        t_list[int(x % t)].append(all_file[x])
    ts = []
    for i in range(t):
        print("队列" + str(i) + "长度:" + str(len(t_list[i])) + " Start!")
        ts.append(threading.Thread(target=save_to_db, args=([t_list[i]])))
    for i in ts:
        i.start()
    for i in ts:
        i.join()


def clear_file_black_word(root):
    with open("../black_word_list.txt", "r", encoding="utf-8") as f_bwl:
        black_word = [x.replace('\n', '') for x in f_bwl.readlines()]
    videos = mysql_util.get_all_video()
    for v in videos:
        name = str(v[1])
        for sub_key in black_word:
            name = name.replace(sub_key, "")
        if not name.startswith("["):
            name = "[" + name

        if name.endswith(".mp4"):
            if not name.endswith("].mp4"):
                name = name.replace(".mp4", "].mp4")

        if name.endswith(".rmvb"):
            if not name.endswith("].rmvb"):
                name = name.replace(".rmvb", "].rmvb")

        if name.endswith(".mkv"):
            if not name.endswith("].mkv"):
                name = name.replace(".mkv", "].mkv")

        name = replace_name(name)
        if v[1] != name:
            print('RENAME:' + str(v[1]))
            print('RE  TO:' + name)
            mysql_util.set_target_name(v[0], name)
    mysql_util.ex_rename()


def rename_file(root, old_str, new_str):
    videos = mysql_util.get_all_video()
    videos = mysql_util.query_video_byname(old_str)
    # videos = mysql.execute("select id,name from video")
    for v in videos:
        name = str(v[1])
        name = name.replace(old_str, new_str)
        print('RENAME:' + str(v[1]))
        print('RE  TO:' + name)
        mysql_util.set_target_name(v[0], name)
    mysql_util.ex_rename()

    # for x in range(99):
    #     if len(str(x)) == 1:
    #         x = '0' + str(x)
    #     x = str(x)
    #     o = '[第' + x + '話]'
    #     n = '[' + x + ']'
    #     videos = mysql_util.query_video_byname(o)
    #     # videos = mysql.execute("select id,name from video")
    #     for v in videos:
    #         name = str(v[1])
    #         name = name.replace(o, n)
    #         # if not name.startswith('['):
    #         #     name = '[' + name
    #         mysql_util.set_target_name(v[0], name)
    #     mysql_util.ex_rename()


def replace_name(name):
    if "OVA" in name:
        if "[OVA" not in name:
            name = name.replace("OVA", "[OVA]")
    name = "[" + name[1:].replace("[", "][")
    name = name.replace("_]", "]")
    name = name.replace("  ", " ")
    name = name.replace("_", " ")
    name = name.replace("2季", "[S2]")
    name = name.replace("一部", "[S1]")
    name = name.replace("-]", "]")
    name = name.replace("1季", "[S1]")
    name = name.replace("第一季", "[S1]")
    name = name.replace("第二季", "[S2]")
    name = name.replace("第三季", "[S3]")
    name = name.replace("12话全", "1-12")
    name = name.replace("13完结", "1-13")
    name = name.replace("12话", "1-12")
    name = name.replace("END]", "][END]")
    name = name.replace(".]", "]")
    name = name.replace("Ⅱ", "[S2")
    name = name.replace("[.", "[")
    name = name.replace(",]", "]")
    name = name.replace("[-", "[")
    name = name.replace("(", "[")
    name = name.replace("（", "[")
    name = name.replace("第", "[")
    name = name.replace("話", "]")
    name = name.replace(")", "]")
    name = name.replace("）", "]")
    name = name.replace("  ", " ")
    name = name.replace(" - ", "][")
    name = name.replace("]]", "]")
    name = name.replace("[[", "[")
    name = name.replace(" ]", "]")
    name = name.replace(" [", "[")
    name = name.replace("[ ", "[")
    name = name.replace("[ ", "[")
    name = name.replace("[]", "")
    name = name.replace("v2]", "]")
    name = name.replace("V2]", "]")
    name = name.replace("[1]", "[01]")
    name = name.replace("[2]", "[02]")
    name = name.replace("[3]", "[03]")
    name = name.replace("[4]", "[04]")
    name = name.replace("[5]", "[05]")
    name = name.replace("[6]", "[06]")
    name = name.replace("[7]", "[07]")
    name = name.replace("[8]", "[08]")
    name = name.replace("[9]", "[09]")
    return name


def cover():
    w_list = [
        'Evangelion',
        '境界线上的地平线',
    ]
    query_sql = 'select v.path,v.name,v.h from video v where file_type="rmvb" order by name DESC '
    videos = mysql.execute(query_sql)
    for x in videos:
        cover_flag = True
        infile = x[0]
        for w in w_list:
            if w in x[0]:
                cover_flag = False
        if cover_flag:
            outfile = os.path.dirname(x[0]) + '/output/' + x[1]
            outfile = outfile.replace(".mp4", ".mkv")
            outfile = outfile.replace(".rmvb", ".mkv")
            outfile = outfile.replace(".avi", ".mkv")
            if not os.path.isfile(outfile):
                if not os.path.isdir(os.path.dirname(x[0]) + '/output/'):
                    os.mkdir(os.path.dirname(x[0]) + '/output/')
                ffmpeg_util.cov_mkv(infile, outfile, x[2])


def rename_dir_byblack(root):
    with open("../black_word_list.txt", "r", encoding="utf-8") as f_bwl:
        black_word = [x.replace('\n', '') for x in f_bwl.readlines()]
    get_all_file(root)
    for dir in all_dir:
        t = Dir(dir)
        if t.path != '':
            new_name = t.name
            for x in black_word:
                new_name = str.replace(new_name, x, '')
            new_name = replace_name(new_name)
            try:
                t.rename(new_name)
            except BaseException:
                print("ERROR: " + t.name + " => " + new_name)


def rename_dir(root, old, new):
    get_all_file(root)
    for dir in all_dir:
        t = Dir(dir)
        if t.path != '':
            t.rename(t.name.replace(old, new))


if __name__ == '__main__':
    root = r'X:/video'
    root = root.replace('\\', '/')
    while True:
        print("*************************************")
        print("     1: rename_dir")
        print("     2: clear_file_black_word")
        print("     3: save_to_db_t")
        print("     4: cover")
        print("     5: rename_dir_byblack")
        print("*************************************")
        print("ROOT: " + os.path.dirname(root))
        print("*************************************")
        sw = int(input("Input A NUM: "))
        if sw == 1:
            rename_dir(root, "[-p]", "")
        elif sw == 2:
            clear_file_black_word(root)
        elif sw == 3:
            save_to_db_t(root, 4)
        elif sw == 4:
            cover()
        elif sw == 5:
            rename_dir_byblack(root)
        else:
            break
        sw = 0
    os.system("pause")
