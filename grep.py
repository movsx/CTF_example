# -*- coding: utf-8 -*-
__author__ = 'Леонид'
import os, time

def preparefllines(fllines):
    fl = []
    for flline in fllines:
        if len(flline.strip()) > 0:
            fl.append(flline.strip())
    return fl

def searchinlines(sllines, fllines):
    for line in sllines:
        for flline in fllines:
            if flline in line:
                print line.strip()
                break

fllines = preparefllines(open("sample").readlines())
seeks = 0
while (1):
    f = open("SyslogFW.txt")
    f.seek(seeks, os.SEEK_SET)
    pts = f.readlines()
    seeks = f.tell()
    searchinlines(pts, fllines)
    f.close()
    time.sleep(10)
