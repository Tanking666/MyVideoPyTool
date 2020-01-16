# -- coding: utf-8 --
import os

from lib.File import File


def is_video(arg):
    return os.path.splitext(arg)[1][1:] in ("mkv", "mp4", "avi", "rmvb")
