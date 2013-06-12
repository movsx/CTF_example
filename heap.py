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

import binascii

### Преобразование ASCII строки с Hexзначениями в буфер
def str2hex(text): # "30313233" = "0123"
    return binascii.a2b_hex(text)

### Преобразование буфера в ASCII строку с Hexзначениями
def hex2str(text): # "0123" = "30313233"
    return binascii.b2a_hex(text)

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

### Преобразование двоичной строки разделенной пробелами в ASCII строку
def bin2str(text): # "110000 110001 110010 110011" = "0123"
    return ''.join( [chr( int( x, 2 ) ) for x in text.split(" ")] )

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


### Пример организации соединения по протоколу Telnet (можно использовать для любых протоколов)
import getpass
import sys
import telnetlib

def sample_telnet():
    HOST = "hostname"
    user = raw_input("Enter your remote account: ")
    password = getpass.getpass()
    tn = telnetlib.Telnet(HOST)
    tn.read_until("login: ") # ждать, пока не придет запрос логина
    tn.write(user + "\n")
    if password:
        tn.read_until("Password: ") # ждать, пока не придет запрос пароля
        tn.write(password + "\n")
    tn.write("ls\n")
    tn.write("exit\n")
    print tn.read_all()

### Пример задачи на сумму цифр с управляющими символами
# условие
###
#    Start reading from right, if digit then add the digit, if 'A' then remove it and go back 2 places, if 'B' then remove and go front 2 places
#    Example : 65a43b21 Answer is 14
#    Solve: 9798781ba143567b89784351b36769689a4949877543623467b8776a424b34a4556787a6542a213457a8865432a5b46569342578ab235912a3985674a2345321895ba01987654032165a43b21
###
# решение
def solve(input, currentPosition=0, currentSum=0):
    if currentPosition >= len(input):
        return currentSum
    elif input[currentPosition].isdigit():
        print "We have a digit:", input[currentPosition]
        return solve(input, currentPosition + 1, currentSum + int(input[currentPosition]))
    elif input[currentPosition] == 'a':
        print "We have 'A'..."
        input.remove(input[currentPosition])
        return solve(input, currentPosition - 1, currentSum)
    elif input[currentPosition] == 'b':
        print "We have 'B'..."
        input.remove(input[currentPosition])
        return solve(input, currentPosition + 3, currentSum)
    else:
        print "Unexpected Result:", input[currentPosition]

def beginSolve():
    toSolve = "9798781ba143567b89784351b36769689a4949877543623467b8776a424b34a4556787a6542a213457a8865432a5b46569342578ab235912a3985674a2345321895ba01987654032165a43b21"
    reverseToSolve = toSolve[::-1]
    print solve(list(reverseToSolve))

### Работа с диском на уровне ОС Windows
# Вызов должен быть ParseDisk(r"\\.\f:") !!! требуются права администратора
import os, sys, re
def grep(pattern,list):
    return filter(pattern.search,list)
def ParseDisk(name):
    import win32file
    import win32con
    BUFFER_SIZE = 2048
    Buffer = 0
    Buffer_Read = BUFFER_SIZE
    hDir = win32file.CreateFile (
        name,
        win32con.GENERIC_READ,
        win32con.FILE_SHARE_READ,
        None,
        win32con.OPEN_EXISTING,
        win32con.FILE_FLAG_BACKUP_SEMANTICS,
        None
    )
    pattern = re.compile("\w{5}");
    data = win32file.AllocateReadBuffer(4096)
    while True:
        result = win32file.ReadFile(hDir, data)
        if not result: break
        print data
        strdata = data
        temp = grep (pattern, strdata)
        if len(temp) > 0: print temp

### Функция перевода чисел из одной системы в другую
# условие задачи: входной файл text
# 1 строка: "из какой системы" "в какую"
# 2 строка: "число"
def perevod_chisel():
    buf = open("text", "r").readlines()
    for i in range(0, len(buf), 2):
        str1, str2 = buf[i:i+2]
        types = str1.split(" ") #types[0] - откуда types[1] - куда
        x = int(str2, int(types[0].strip()))
        int2 = int(types[1].strip())
        n=""
        while x > 0:
            y, x = x % int2, int(x / int2)
            if y < 10:
                q = str(y)
            else:
                q = chr(ord("A")+y-10)
            n = q + n
        print (n)

### Функция переворота строки
# при входе primer 1 вернет 1 remirp
def reversestr(str):
    return str[::-1]

### Аналог функций random и seed из библиотеки glibc
# Очень медленная в rand.cpp на 2 порядка быстрее
def rands(seed):
    r = []
    r.append(seed)
    for i in range(1,31):
        r.append((16807 * r[i-1]) % 2147483647)
        if (r[i] < 0):
            r[i] += 2147483647

    for i in range(31, 34):
        r.append(r[i-31])

    for i in range(34, 344):
        r.append((r[i-31] + r[i-3]) &0xffffffff)

    for i in range(344, 355):
        r.append((r[i-31] + r[i-3])  &0xffffffff)
        print(r[i])

### Добавлена функция декодирования ROT-13
def rot13(str):
    return str.decode('rot-13')

### Функция парсит буффер на вхождение вида {\*\volgactf0XXXXX}
# задача была по выявлению из rtf-файла невидимого jpg
def parsertf(text):
    f = open("result", "w")
    for i in range(0, 1000):
        s = r"{\*\volgactf%i " % (i)
        begin = text.find(s)
        if begin == -1:
            print i
            break
        end = text.find("}", begin)
        str = text[begin+len(s):end]
        f.write(str)
    f.close()

### Нерекурсивная функция обхода ФС для сбора файла
# задача: в каталоге верхнего уровня подкоталоги буквы
# в каждом из них файл, с указанием места, где этот символ встречается.
# требуется собрать файл в кучу
# Пройти по каталогам первого уровня. Собрать все
def walk():
    import sys, os
    q = list(1500 * " ") # вырожденно добавляем больщой буффер, т.к. символы добавляется не последовательно
    for name in os.listdir("admin100"):
        t = name
        if t == "coma":
            t = ","
        if t == "dot":
            t = "."
        if t == "quote":
            t = '"'
        if t == "space":
            t = " "
        path = os.path.join("admin100", name, "file")
        f = open(path)
        lines = f.readlines()
        for line in lines:
            q[int(line)] = t
        f.close()
    pts = open("asd", "w")
    for i in q:
        pts.write(i)
    pts.close()

### Еще одна нерекурсивная функция обхода файловой системы до 8 уровня вложенности
# задача: в том, что 8 уровней вложенности составляют байт, если он есть в ключе, то внутри директории есть файл, который
# указывает место, где он хранится
def walk2():
    q = list(20 * " ")
    for name in os.listdir("forest"):
        path = os.path.join("forest", name)
        for name2 in os.listdir(path):
            path2 = os.path.join(path, name2)
            for name3 in os.listdir(path2):
                path3 = os.path.join(path2, name3)
                for name4 in os.listdir(path3):
                    path4 = os.path.join(path3, name4)
                    for name5 in os.listdir(path4):
                        path5 = os.path.join(path4, name5)
                        for name6 in os.listdir(path5):
                            path6 = os.path.join(path5, name6)
                            for name7 in os.listdir(path6):
                                path7 = os.path.join(path6, name7)
                                for name8 in os.listdir(path7):
                                    path8 = os.path.join(path7, name8, "end.txt")

                                    f = open(path8)
                                    lines = f.read()
                                    if lines.find("key_part") > 0:
                                        ps = int(lines[0:2])
                                        print ps
                                        ts = name + name2 + name3 + name4 + name5 + name6 + name7 +name8
                                        print ts
                                        q[ps] = chr(int(ts,2))
                                        print q[ps]
                                    f.close()
    print str(q)

rands(1)