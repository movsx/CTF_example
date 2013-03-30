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

### XOR для буфера по ключу меньше, чем буфер
def many_byte_xor(buf, key):
    buf = bytearray(buf)
    for i, bufbyte in enumerate(buf):
        buf[i] = chr(bufbyte ^ ord(key[i % len(key)]))
    return str(buf)

### Преобразование ASCII кодов в 16-ричном виде в ASCII строку
import binascii
def dehex():
    fq=open ("sniffed.dehex2", "wb+")
    for i in open("sniffed.hex", 'rb').readlines():
        fq.write(binascii.a2b_hex(i.strip())) # сама функция, отвечающая за преобразование строки вида 313233 в 123
    fq.close()

### Подсчет КС по алгоритму hashSHA384
import hashlib
def hashSHA384(msg):
    return hashlib.sha384(msg).hexdigest()

### Работа со struct (подробно формат описан http://docs.python.org/dev/library/struct.html)
from struct import pack, unpack
def prosto_struct():
    f = open("text.bin", "wb+")
    f.write(pack('hh', 1, 2))  # h - код для короткого целого со знаком
    print unpack('bbbb', 'ABCD')  # b соответствует символу со знаком
    f.write(pack('!l', 1025))  # сетевой (от старшего к младшему, big-endian)
    f.write(pack('>l', 1025))  # от старшего к младшему, big-endian
    f.write(pack('<l', 1025))  # от младшего к старшему, little-endian # родной для i386

### Работа с путями
import os.path
def prosto_path():
    print os.path.join("/tmp/1", "temp.file")  # конкатенация путей /tmp/1\temp.file
    print os.path.dirname("/tmp/1/temp.file")  # имя каталога по заданному полному пути /tmp/1
    print os.path.basename("/tmp/1/temp.file")  # имя файла по заданному полному пути temp.file
    print os.path.normpath("/tmp//2/../1/temp.file")  # нормализация пути '/tmp/1/temp.file'
    print os.path.exists("/tmp/1/temp.file")  # существует ли путь? False

### Полезные функции из модуля string
import string
def prosto_string_const():
    print string.ascii_letters #строка, содержащая все буквы из набора ASCII
    print string.ascii_lowercase
    print string.digits # строка с цифрами от 0 до 9
    print string.letters # буквы, зависят от установки локали

### Функции подстановки в строки по ключевым словам
from string import Template
def prosto_string_template():
    tpl = Template("""${name} has ${amount}$$. {oh}""")
    print tpl.substitute({"amount": 100, "name": "John"}) # 'John has 100$. {oh}'
    print tpl.safe_substitute({"amount": 100}) # '${name} has 100$. {oh}'
    print """{name} has {amount}$. {{oh}}""".format(**{"amount": 100, "name": "John"}) # 'John has 100$. {oh}'

### Поддержка регулярных выражений: модуль re
# Модуль re содержит функции для замены (sub), разбиения строки (split), сравнения строки с шаблоном (match, search),
# поиска (finditer, findall)
import re
def prosto_re():
    compiled_re = re.compile(r"[a-b][0-9]*")
    print [m.group(0) for m in compiled_re.finditer("A1 c123 a12, b abc (b987).")] #['a12', 'b', 'a', 'b', 'b987']

### Пример чтения и записи файла в формате CSV
import csv
def prosto_csv():
    reader = csv.reader(open("some.csv", "rb"))
    for row in reader:
        print row

    # Модуль позволяет настроить формат читаемых и записываемых файлов. Например можно выставить разделитель полей :, разделитель строк — |, символ цитирования — ` (вместо " по умолчанию).
    writer = csv.writer(open("some.csv", "wb"), delimiter=':', quoting=csv.QUOTE_MINIMAL, quotechar='`', lineterminator='|')
    writer.writerows([ [1997, "Ford", "E350", "ac, abs, moon", "3000.00"],
                       [1999, "Chevy", "Venture `Extended Edition`", "", "4900.00"],
                       [1996, "Jeep", "Grand Cherokee", "air, moon roof, loaded MUST SELL!", "4799.00"] ])

### Работа с файловыми архивами
from zipfile import ZipFile
def prosto_zip():
    # В следующем примере в файле archive.zip будет заархивирован файл file.txt, содержащий текст «text in the file»
    with ZipFile('archive.zip', 'w') as ziparc:
        ziparc.writestr('file.txt', 'text in the file')

    # Чтение архива происходит аналогично. В следующем примере будут напечатаны имена файлов, содержащиеся в архиве:
    with ZipFile('archive.zip', 'r') as ziparc:
        for fileinfo in ziparc.filelist:
            print(fileinfo.filename)

prosto_zip()
