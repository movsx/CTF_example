# -*- coding: utf-8 -*-
# __author__ = 'movsx'

### Простой пример разбора файла на части по заголовку
import re, sys
def findheadersinfile():
    data = open("35e25782a7b3b88409e58756e63c40c2", "rb").read()
    gzip_offsets = [m.start() for m in re.finditer('\x1f\x8b', data)] # собираем все смещения заголовка gz файла в буффере
    for i in xrange(len(gzip_offsets)-1): # от 1 до предпоследнего
        start, end = gzip_offsets[i:i+2] # [хватаем начало, конец из массива смещений
        open('p/%03d.gz' % i, 'w').write(data[start:end]) # записываем от начала до конца в новые файлы

### XOR для одинаковых строк
def xor_strings(xs, ys):
    return "".join(chr(ord(x) ^ ord(y)) for x, y in zip(xs, ys))

