# -- coding: utf-8 --
import os
from datetime import time
from time import sleep

import MySQLdb
from DBUtils.PooledDB import PooledDB
from lib import Config


# conn = pool.connection()  # 以后每次需要数据库连接就是用connection（）函数获取连接就好了
# cur = conn.cursor()
# SQL = "select * from table1"
# r = cur.execute(SQL)
# r = cur.fetchall()
# cur.close()
# conn.close()


class MysqlUtil(object):

    @staticmethod
    def get_pool():
        return PooledDB(creator=MySQLdb, mincached=1, maxcached=5,
                        host=Config.DBHOST, port=Config.DBPORT, user=Config.DBUSER, passwd=Config.DBPWD,
                        db=Config.DBNAME, use_unicode=True, charset=Config.DBCHAR)

    def __init__(self):
        self.pool = MysqlUtil.get_pool()

    def get_conn(self):
        return self.pool.connection()

    def execute(self, sql):
        conn = self.pool.connection()
        cur = conn.cursor()
        count = cur.execute(sql)
        r = cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()
        return r

    def execute_t(self, sqls):
        conn = self.pool.connection()
        cur = conn.cursor()
        r = []
        try:
            for sql in sqls:
                cur.execute(sql)
                r.append(cur.fetchall())
        except BaseException:
            print("[ERROR]SQL:" + sqls)
            conn.rollback()
        else:
            conn.commit()
        finally:
            cur.close()
            conn.close()
        return r


mysql = MysqlUtil()


def refrash_data():
    # resql = "UPDATE video v SET v.target_name = REGEXP_REPLACE(v.name,'\\[[0-9,A-F]{4,8}\\]','') WHERE v.name REGEXP '\\[[0-9,A-F]{4,8}\\]';"
    # mysql.execute(resql)
    sql = "select path,id,size,file_name from video"
    data = mysql.execute(sql)
    del_list = []
    for x in data:
        if not os.path.isfile(x[0]):
            del_list.append(x[1])
        elif os.path.getsize(x[0]) != x[2]:
            del_list.append(x[1])
        elif not os.path.isfile(x[3]):
            del_list.append(x[1])

    if len(del_list) > 0:
        del_list = str(del_list)[1:]
        del_list = del_list[:-1]
        mysql.execute("delete from video where id in (%s)" % (del_list,))
    mysql.execute("UPDATE video v set v.rate20 = v.size/v.len/v.h/v.w*20*60 where v.rate20 is null")
    print("Clean Work DONE!!")


def get_all_video():
    res = mysql.execute("select id,name,path from video")
    return res


def get_all_video_hw():
    res = mysql.execute("select id,name,w,h from video")
    return res


def resub_all_video():
    res = mysql.execute("select id,sub_group from video where sub_group is not null")

    for x in res:
        subs = x[1]
        subs = subs.replace("][", "]$$[")
        subs = subs.split("$$")
        subs = set(subs)
        sub = ''
        for xx in subs:
            sub = sub + xx
        mysql.execute('update video v set v.sub_group="%s" where v.id="%s"' % (sub, x[0]))


def query_video_byname(name):
    res = mysql.execute('select id,name,h,p_name from video where name like "%' + name + '%"')
    return res


def set_target_name(vid, target_name):
    try:
        mysql.execute('update video set target_name="%s" where id ="%s"' % (target_name, vid))
    except:
        print("[ERROR] SQL:" + 'update video set target_name="%s" where id ="%s"' % (target_name, vid))


def set_subgroup(vid, sub_group):
    try:
        sql = 'update video v set v.sub_group=concat(ifnull(v.sub_group,""),"%s")  where id ="%s"' % (sub_group, vid)
        mysql.execute(sql)
    except:
        print("[ERROR] SQL:" + sql)


def ex_rename():
    print("[INFO] Start Rename")
    data = mysql.execute(
        'select path,concat(replace(path,name,""),target_name) as n_path,id from video where target_name is not null')
    for x in data:
        try:
            os.rename(x[0], x[1])
        except BaseException:
            print("[ERROR] RENAME:" + x[0] + " => " + x[1])
            continue
        else:
            try:
                sqls = [
                    'update video set path=replace(path,name,target_name) where id ="%s"' % x[2],
                    'update video set name=target_name , file_name=target_name where id ="%s"' % x[2],
                    'update video set target_name=null where id ="%s"' % x[2]]
                mysql.execute_t(sqls)
            except BaseException:
                os.rename(x[1], x[0])


def get_name_bysize_pname(pname, size):
    sql = 'SELECT v.name FROM video v WHERE v.path LIKE "%' + pname + '%" AND v.size=' + str(size)
    data = mysql.execute(sql)
    return data[0][0]


if __name__ == '__main__':
    # resub_all_video()
    # os.rename("X:/Video/1TV/[2012]/[2012][冰菓]/[冰果][Hyouka][01][].mp4","X:/Video/1TV/[2012]/[2012][冰菓]/[冰果][Hyouka][01].mp4")
    # refrash_data()
    ex_rename()
    # refrash_data()