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
# Format 	C Type 	        Python type 	Standard size
#   x 	    pad byte 	    no value
#   c 	    char 	        bytes of length     1
#   b 	    signed char 	integer 	        1
#   B 	    unsigned char 	integer 	        1
#   ? 	    _Bool 	        bool 	            1
#   h 	    short 	        integer 	        2
#   H 	    unsigned short 	integer 	        2
#   i 	    int 	        integer 	        4
#   I 	    unsigned int 	integer 	        4
#   l 	    long 	        integer 	        4
#   L 	    unsigned long 	integer 	        4
#   q 	    long long 	    integer 	        8
#   Q 	    unsigned long long 	integer 	    8
#   n 	    ssize_t 	    integer
#   N 	    size_t 	        integer
#   f 	    float 	        float 	            4
#   d 	    double 	        float 	            8
#   s 	    char[] 	        bytes
#   p 	    char[] 	        bytes
#   P 	    void * 	        integer

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
    print string.hexdigits # 0-9a-fA-F

### Функции для работы с форматированием строк
def prosto_string_format():
    print '{:<30}'.format('left aligned') # 'left aligned                  '
    print '{:>30}'.format('right aligned') # '                 right aligned'
    print '{:^30}'.format('centered') # '           centered           '
    print '{:*^30}'.format('centered')  # use '*' as a fill char # '***********centered***********'
    # format also supports binary numbers
    print "int: {0:d};  hex: {0:x};  oct: {0:o};  bin: {0:b}".format(42) # 'int: 42;  hex: 2a;  oct: 52;  bin: 101010'
    # with 0x, 0o, or 0b as prefix:
    print "int: {0:d};  hex: {0:#x};  oct: {0:#o};  bin: {0:#b}".format(42) # 'int: 42;  hex: 0x2a;  oct: 0o52;  bin: 0b101010'
    # Expressing a percentage
    points = 19.5
    total = 22
    print 'Correct answers: {:.2%}'.format(points/total) # 'Correct answers: 88.64%'

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

### преобразование строки в массив битов
def str2bits(open_text):
    bts = []
    # bin(ord("A")) = 0b1000001, поэтому [2:] мы отбросим 0b и получим 7 знаков
    # '00000000'[len(bin(ord(c))[2:]):] - мы получим один 0, который у нас расширяет до 8 символов
    # напечатать просто 8 значное представление будет
    # print ['00000000'[len(bin(ord(c))[2:]):] + bin(ord(c))[2:] for c in "ABC"]
    [bts.extend([int(b) for b in '00000000'[len(bin(ord(c))[2:]):] + bin(ord(c))[2:]]) for c in open_text]
    return bts

### преобразование массива битов в ASCII строку
def bits2str(bits):
    chars = []
    for b in range(len(bits) / 8):
        byte = bits[b*8:(b+1)*8]
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
    return ''.join(chars)

### пример шифрования симметричными ключами
def crypt():
    text = "0123456789ABCDEF"
    params = [1,2,3,4,5,6,7,8,1,2,3,4,5,6,7,8,1,2,3,4,5,6,7,8,1,2,3,4,5,6,7,8,1,2,3,4,5,6,7,8,1,2,3,4,5,6,7,8,
              1,2,3,4,5,6,7,8,1,2,3,4,5,6,7,8,1,2,3,4,5,6,7,8,1,2,3,4,5,6,7,8,1,2,3,4,5,6,7,8,1,2,3,4,5,6,7,8,
              1,2,3,4,5,6,7,8,1,2,3,4,5,6,7,8,1,2,3,4,5,6,7,8,1,2,3,4,5,6,7,8]
    bts = []
    # обрабатываем по 16*8 (128) бит открытого кода за раз
    # blk for blk in [bts[i * 128:(i+1) * 128] for i in range(len(text) // 16)]
    [bts.extend([int(b) for b in '00000000'[len(bin(ord(c))[2:]):] + bin(ord(c))[2:]]) for c in text]
    print [blk for blk in [bts[i * 128:(i+1) * 128] for i in range(len(text) // 16)]]
    # params - должен содержать обязательно 128 значений, мы пробегаемся по каждому биту и умножаем на ключ из params
    print [map(lambda x: x[0] * x[1] ,zip(blk, params)) for blk in [bts[i * 128:(i+1) * 128] for i in range(len(text) // 16)]]
    # затем все это суммируем
    print [sum(map(lambda x: x[0] * x[1] ,zip(blk, params))) for blk in [bts[i * 128:(i+1) * 128] for i in range(len(text) // 16)]]
    return [sum(map(lambda x: x[0] * x[1] ,zip(blk, params))) for blk in [bts[i * 128:(i+1) * 128] for i in range(len(text) // 16)]]

crypt()
#print bits2str(str2bits("Hello_world"))
