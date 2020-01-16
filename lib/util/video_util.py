import os
import sys
import xlwt
from moviepy.editor import VideoFileClip


def get_filesize(filename):
    """
    获取文件大小（M: 兆）
    """
    file_byte = os.path.getsize(filename)
    return sizeConvert(file_byte)


def get_file_timecn(filename):
    """
    获取视频时长（s:秒）
    """
    clip = VideoFileClip(filename)
    file_time = timeConvert(clip.duration)
    return file_time


def get_file_sec(filename):
    """
    获取视频时长（s:秒）
    """
    clip = VideoFileClip(filename)
    sec = clip.duration
    clip.close()
    return sec


def sizeConvert(size):  # 单位换算
    K, M, G = 1024, 1024 ** 2, 1024 ** 3
    if size >= G:
        return str(size / G) + 'G Bytes'
    elif size >= M:
        return str(size / M) + 'M Bytes'
    elif size >= K:
        return str(size / K) + 'K Bytes'
    else:
        return str(size) + 'Bytes'


def timeConvert(size):  # 单位换算
    M, H = 60, 60 ** 2
    if size < M:
        return str(size) + u'秒'
    if size < H:
        return u'%s分钟%s秒' % (int(size / M), int(size % M))
    else:
        hour = int(size / H)
        mine = int(size % H / M)
        second = int(size % H % M)
        tim_srt = u'%s小时%s分钟%s秒' % (hour, mine, second)
        return tim_srt


# def get_all_file(self):
#     u"""
#     获取视频下所有的文件
#     """
#     for root, dirs, files in os.walk(file_dir):
#         return files  # 当前路径下所有非目录子文件


if __name__ == '__main__':
    filename = r"X:\Video\[2018][粗点心战争2][Dagashi Kashi 2][01-12END][GB&JP][720P]\[Nekomoe kissaten][Dagashi Kashi 2][01][GB&JP][720P].mp4"
    print()
