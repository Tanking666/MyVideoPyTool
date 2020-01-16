# -- coding: utf-8 --
import os
import re
import subprocess

# cmd = r'"ffmpeg -i "X:\Video\1TV\[2018]\[2018][A.I.C.O. Incarnation]\[A.I.C.O. Incarnation][1][1080P].mkv" -map 0:0 -map 0:1 -map 0:2 -crf 20 -r 23.976 -c:v h264_nvenc -ar:1 44100 -b:a:1 192k -c:a:1 aac -ar:2 44100 -b:a:2 192k -c:a:2 aac -y "d:\[2018][A.I.C.O. Incarnation]\a.mkv"'

FFMPEG = r'"D:\Program Files\Tools_App\ffmpeg\bin\ffmpeg.exe" '


def cov_1080p(infile, outfile):
    ai = 1
    try:
        inStream = InStream(infile)
        ai = inStream.stream_cnt - 1
    except BaseException:
        pass
    cmdc = FFMPEG
    cmdc += '-y -i "'
    cmdc += infile + '" '
    # cmd_audio = ' -crf 20 -r 23.976 '
    cmd_audio = ''
    cmd_video = ' -b:v 3600k -r 23.976 -c:v:0 hevc_nvenc -max_muxing_queue_size 10240 '
    cmd_map = ' -map 0:0 '
    for x in range(ai):
        cmd_map += ' -map 0:%s ' % str(x + 1)
        cmd_audio += ' -ar:%s 44100 -b:a:%s 192k -c:a:%s aac ' % (str(x + 1), str(x + 1), str(x + 1),)
    cmdc += cmd_map
    cmdc += cmd_audio
    cmdc += cmd_video
    cmdc += '"' + outfile + '"'
    print(cmdc)
    ps = subprocess.Popen(cmdc)
    ps.wait()


def cov_1080pp(infile, outfile, ai=1):
    cmdc = FFMPEG
    cmdc += '-y -i "'
    cmdc += infile + '" '
    # cmd_audio = ' -crf 20 -r 23.976 '
    cmd_audio = ''
    cmd_video = ' -b:v 9999k -r 23.976 -c:v:0 hevc_nvenc -max_muxing_queue_size 10240 '
    cmd_map = ' -map 0:0 '
    for x in range(ai):
        cmd_map += ' -map 0:%s ' % str(x + 1)
        cmd_audio += ' -ar:%s 44100 -b:a:%s 192k -c:a:%s aac ' % (str(x + 1), str(x + 1), str(x + 1),)
    cmdc += cmd_map
    cmdc += cmd_audio
    cmdc += cmd_video
    cmdc += '"' + outfile + '"'
    print(cmdc)
    ps = subprocess.Popen(cmdc)
    ps.wait()


def cov_mkv(infile, outfile, h):
    rate = int(2500 / 1080 / 1920 * int(h) / 9 * 16 * int(h))
    cmdc = FFMPEG
    cmdc += '-y -i "'
    cmdc += infile + '" '
    # cmd_audio = ' -crf 20 -r 23.976 '
    cmd_audio = ''
    cmd_video = ' -b:v ' + str(rate) + 'k -c:v hevc_nvenc '
    cmd_map = ''
    cmd_audio += ' -c:a copy '
    cmdc += cmd_map
    cmdc += cmd_audio
    cmdc += cmd_video
    cmdc += '"' + outfile + '"'
    print(cmdc)
    ps = subprocess.Popen(cmdc)
    ps.wait()


class Stream:
    def __init__(self, stype):
        self.stype = stype
        self.codetype = ''
        self.rate = 0
        self.w = 0
        self.h = 0


class InStream:
    def __init__(self, path):
        self.path = path
        self.file_name = ''
        self.streams = []
        self.v_stream = Stream('v')
        self.len = 0
        self.stream_cnt = 0
        self.info = self.get_info()

    def get_info(self):
        cmdc = FFMPEG
        cmdc += ' -i "' + self.path + '" '
        proc = subprocess.Popen(cmdc, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out = proc.stderr
        info = ''
        for x in out:
            line = str(x, encoding="utf-8", errors="ignore")
            info += line
            if line.startswith("Input #"):
                self.file_name = line[line.find("from '") + 6:-4]
            elif line.startswith("    Stream #0:"):
                if "Video" in line:
                    self.stream_cnt = self.stream_cnt + 1
                    l = line[line.index("Video:") + 6:-1].split(',')
                    self.v_stream.codetype = l[0]
                    b = re.search(r"(\d\d\d\d?)x(\d\d\d\d?)", line)
                    self.v_stream.w = int(b.group(1))
                    self.v_stream.h = int(b.group(2))
                elif "Audio" in line:
                    self.stream_cnt = self.stream_cnt + 1
            if line.startswith("  Duration:"):
                tl = line[12:20].split(":")
                len = int(tl[0]) * 3600 + int(tl[1]) * 60 + int(tl[2])
                self.len = len
                # elif "Audio" in line:
                #     s = Stream("a")
                #     self.streams.append(s)

        return info


if __name__ == '__main__':
    infile = r'X:/video/2合集/[2000-2005]/[2004][双恋1+2][H][480p][acc]/[双恋2][05].mkv'

    outfile = 'D:/3.mkv'
    cov_mkv(infile, outfile)
    # print(vs.info)
