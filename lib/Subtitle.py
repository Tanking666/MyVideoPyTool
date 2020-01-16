# -- coding: utf-8 --
import os
import uuid

from lib.File import File

from lib.util import common_util, mysql_util
from lib.util.ffmpeg_util import InStream

mysql = mysql_util.MysqlUtil()


class Subtitle(File):
    def __init__(self, path):
        super().__init__(path)
        if self.path != '':
            if self.exten in ("idx", "sub", "ssa", "rmvb"):
                self.type = "video"
                self.id = ""
                self.length = 0
                self.p_name = os.path.basename(os.path.dirname(self.path))
                self.h = 0
                self.w = 0
                self.fps = 0
                self.video_name = self.name
            else:
                self.path = ''

    def init_byid(self):

        query_sql = 'SELECT v.id,v.name,v.p_name,v.size,v.md5,v.path,v.file_type,v.len,v.h,v.w,v.fps,v.file_name FROM video v where id="%s"' % (
            self.id)
        try:
            data = mysql.execute(query_sql)
        except BaseException:
            print('[ERROR]query_sql=>' + query_sql)
        else:
            self.name = data[0][1]
            self.p_name = data[0][2]
            self.size = data[0][3]
            self.md5 = data[0][4]
            self.path = data[0][5]
            self.exten = data[0][6]
            self.length = data[0][7]
            self.h = data[0][8]
            self.w = data[0][9]
            self.fps = data[0][10]
            self.video_name = data[0][1]
            # print('已存在:' + self.path)

    def get_video_info(self):
        if self.length == 0:
            try:
                vs = InStream(self.path)
                self.length = vs.len
                self.h = vs.v_stream.h
                self.w = vs.v_stream.w
                self.fps = 0
            except BaseException:
                print("[ERROR]Cant Open :" + self.path)


    def save_or_update(self):
        if self.path != '':
            tsql = 'select id from video where name="%s" and size=%s' % (self.name, self.size)
            data = ()
            try:
                data = mysql.execute(tsql)
            except BaseException:
                print('[ERROR]tsql=>' + tsql)
            if len(data) > 0:
                self.id = data[0][0]
                self.init_byid()
            else:
                self.id = uuid.uuid1()
                self.get_video_info()
                self.get_md55()
                sql = 'INSERT INTO video (id, name, p_name, size, md5, path, file_type, `len`,h,w,fps,file_name) VALUES ("%s", "%s", "%s", %s, "%s", "%s", "%s", "%s", "%s", "%s", %s, "%s");' % (
                    self.id, self.name, self.p_name, self.size, self.md5, self.path, self.exten,
                    self.length, self.h, self.w, self.fps, self.name)
                try:
                    mysql.execute(sql)
                    print("[INFO] INSERT:" + self.md5 + '  ' + self.path)
                except BaseException:
                    print('[ERROR]sql=>' + sql)


if __name__ == '__main__':
    v = Video(r"X:/Video/2合集/[2006-2010]/[2006][Fate_Stay_Night+UBW+Fate_Zero 合集][BDRIP][720P][X264-10bit_AAC]/[异域-11番小队][Fate_Unlimited_Blade_Works][00-25+MOVIE+GE+SP][BDRIP][720P][X264-10bit_AAC]/[Fate Unlimited Blade Works][15][BDRIP][X264][10bit][AAC][00][BDRIP][D919].mp4")
    v.save_or_update()
