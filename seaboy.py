# -*- coding: utf-8 -*-
import struct
import socket
import sys
from numpy import *
import time

def flagmas(x,y,z):
    if (x-1 >= 0):
        if (y-1 >= 0):
            if (z-1 >= 0):
                massive[x-1, y-1, z-1] = 1
            massive[x-1, y-1, z] = 1
            if (z+1 < 10):
                massive[x-1, y-1, z+1] = 1
        if (z-1 >= 0):
            massive[x-1, y, z-1] = 1
        massive[x-1, y, z] = 1
        if (z+1 < 10):
            massive[x-1, y, z+1] = 1
        if (y+1 < 10):
            if (z-1 >= 0):
                massive[x-1, y+1, z-1] = 1
            massive[x-1, y+1, z] = 1
            if (z+1 < 10):
                massive[x-1, y+1, z+1] = 1

    if (y-1 >= 0):
        if (z-1 >= 0):
            massive[x, y-1, z-1] = 1
        massive[x, y-1, z] = 1
        if (z+1 < 10):
            massive[x, y-1, z+1] = 1
    if (z-1 >= 0):
        massive[x, y, z-1] = 1
    if (z+1 < 10):
        massive[x, y, z+1] = 1
    if (y+1 < 10):
        if (z-1 >= 0):
            massive[x, y+1, z-1] = 1
        massive[x, y+1, z] = 1
        if (z+1 < 10):
            massive[x, y+1, z+1] = 1

    if (x+1 < 10):
        if (y-1 >= 0):
            if (z-1 >= 0):
                massive[x+1, y-1, z-1] = 1
            massive[x+1, y-1, z] = 1
            if (z+1 < 10):
                massive[x+1, y-1, z+1] = 1
        if (z-1 >= 0):
            massive[x+1, y, z-1] = 1
        massive[x+1, y, z] = 1
        if (z+1 < 10):
            massive[x+1, y, z+1] = 1
        if (y+1 < 10):
            if (z-1 >= 0):
                massive[x+1, y+1, z-1] = 1
            massive[x+1, y+1, z] = 1
            if (z+1 < 10):
                massive[x+1, y+1, z+1] = 1

def vistrel(x,y,z):
    q = "%i:%i:%i\n" % (int(x),int(y),int(z))
    s.send(q) # отправляем координату
    try:
        a = s.recv(4096) # выводим на экран принятый ответ
    except:
        print "lost signal", masko
        return 0
    print >>f, q.strip(), a.strip()
    massive[x][y][z] = 1
    if (a.strip()=="Hit"): # ранили
        return 1
    if (a.strip()=="Hit and Die"): # подбили
        return 2
    if (a.strip()=="You win! Play again"):
        return 4
    return 0

def dobivxvr(x,y,z):    # по x вперед
    if (x + 1 > 9 or massive[x+1][y][z] > 0):
        return 0

    minx = maxx = x; miny = maxy = y; minz = maxz = z # запоминаем координаты
    # стреляем
    res = vistrel(maxx+1,y,z)
    if (res == 0):
        return 0
    if (res == 4):
        return 4
    maxx += 1
    if (res==1): # ранили
        #print "Ранили" # теперь не может быть несколько направлений, фиксируем x
        for ps in range(2): # не больше 4 палубника, а уже 2 подбили
            # по x вперед
            if (maxx + 1 > 9 or massive[maxx+1][y][z] > 0):
                break
            res = vistrel(maxx+1,y,z)
            if (res==0): # промазали, значит вперед, добиваем
                break
            if (res == 4):
                return 4
            maxx += 1
            if (res<>1): # ранили
                break
        if (res < 2): # еще не убили, значит вперед по x
            for ps in range(2): # не больше 4 палубника, а уже 2 подбили
                # по x назад
                if (minx - 1 < 0 or massive[minx-1][y][z] > 0):
                    print "ERRRROR2!!!"
                    break
                res = vistrel(minx-1,y,z)
                if (res == 4):
                    return 4
                minx -= 1
                if (res<>1): # не ранили
                    break
    if (res <> 2):
        print "ERRRROR3!!!"
        return 0
        # подбили
    dlin = maxx-minx+1
    masko[dlin-1] -= 1
    #print "Осталось толстушек(%i): %i" % (dlin, masko[dlin-1])
    for fds in range(minx, maxx+1):
        flagmas(fds,y,z)
    return 1

def dobivyvr(x,y,z):    # по y вперед
    if (y + 1 > 9 or massive[x][y+1][z] > 0): # тупиковая ситуация с кораблем
        return 0

    minx = maxx = x; miny = maxy = y; minz = maxz = z # запоминаем координаты
    # стреляем
    res = vistrel(x,y+1,z)
    if (res == 0):
        return 0
    if (res == 4):
        return 4
    maxy += 1
    if (res==1): # ранили
        #print "Ранили" # теперь не может быть несколько направлений, фиксируем x
        for ps in range(2): # не больше 4 палубника, а уже 2 подбили
            # по x вперед
            if (maxy + 1 > 9 or massive[x][maxy+1][z] > 0):
                break
            res = vistrel(x,maxy+1,z)
            if (res == 4):
                return 4
            if (res==0): # промазали, значит назад, добиваем
                break
            maxy += 1
            if (res<>1): # ранили
                break
        if (res < 2): # еще не убили, значит вперед по x
            for ps in range(2): # не больше 4 палубника, а уже 2 подбили
                # по y назад
                if (miny - 1 < 0 or massive[x][miny-1][z] > 0):
                    print "ERRRROR2!!!"
                    break
                res = vistrel(x,miny-1,z)
                if (res == 4):
                    return 4
                miny -= 1
                if (res<>1): # не ранили
                    break
    if (res <> 2):
        print "ERRRROR3!!!"
        return 0
        # подбили
    dlin = maxy-miny+1
    masko[dlin-1] -= 1
    #print "Осталось толстушек(%i): %i" % (dlin, masko[dlin-1])
    for fds in range(miny, maxy+1):
        flagmas(x, fds,z)
    return 1

def dobivzvr(x,y,z):    # по z вперед
    if (z + 1 > 9 or massive[x][y][z+1] > 0):
        return 0

    minx = maxx = x; miny = maxy = y; minz = maxz = z # запоминаем координаты
    # стреляем
    res = vistrel(x,y,z+1)
    if (res == 4):
        return 4
    if (res == 0):
        return 0
    maxz += 1
    if (res==1): # ранили
        #print "Ранили" # теперь не может быть несколько направлений, фиксируем x
        for ps in range(2): # не больше 4 палубника, а уже 2 подбили
            if (maxz + 1 > 9 or massive[x][y][maxz+1] > 0):
                break
            res = vistrel(x,y,maxz+1)
            if (res == 4):
                return 4
            if (res==0): # промазали, значит назад, добиваем
                break
            maxz += 1
            if (res<>1): # ранили
                break
        if (res < 2): # еще не убили, значит вперед по x
            for ps in range(2): # не больше 4 палубника, а уже 2 подбили
                # по z назад
                if (minz - 1 < 0 or massive[x][y][minz-1] > 0): # тупиковая ситуация с кораблем
                    print "ERRRROR2!!!"
                    break
                res = vistrel(x,y,minz-1)
                if (res == 4):
                    return 4
                minz -= 1
                if (res<>1): # не ранили
                    break
    if (res <> 2):
        print "ERRRROR3!!!"
        return 0
        # подбили
    dlin = maxz-minz+1
    masko[dlin-1] -= 1
    #print "Осталось толстушек(%i): %i" % (dlin, masko[dlin-1])
    for fds in range(minz, maxz+1):
        flagmas(x, y, fds)
    return 1

def dobivxvl(x,y,z):    # по x назад
    if (x - 1 < 0 or massive[x-1][y][z] > 0):
        return 0

    minx = maxx = x; miny = maxy = y; minz = maxz = z # запоминаем координаты
    # стреляем
    res = vistrel(minx-1,y,z)
    if (res == 4):
        return 4
    if (res == 0):
        return 0
    minx -= 1
    if (res==1): # ранили
 #       print "Ранили" # теперь не может быть несколько направлений, фиксируем x
        for ps in range(2): # не больше 4 палубника, а уже 2 подбили
            # по x назад
            if (minx - 1 < 0 or massive[minx-1][y][z] > 0):
                break
            res = vistrel(minx-1,y,z)
            if (res == 4):
                return 4
            if (res==0): # промазали, значит вперед, добиваем
                break
            minx -= 1
            if (res<>1): # ранили
                break
        if (res < 2): # еще не убили, значит вперед по x
            for ps in range(2): # не больше 4 палубника, а уже 2 подбили
                # по x вперед
                if (maxx + 1 > 9 or massive[maxx+1][y][z] > 0):
                    print "ERRRROR2!!!"
                    break
                res = vistrel(maxx+1,y,z)
                if (res == 4):
                    return 4
                maxx += 1
                if (res<>1): # не ранили
                    break
    if (res <> 2):
        print "ERRRROR3!!!"
        return 0
    # подбили
    dlin = maxx-minx+1
    masko[dlin-1] -= 1
#    print "Осталось толстушек(%i): %i" % (dlin, masko[dlin-1])
    for fds in range(minx, maxx+1):
        flagmas(fds,y,z)
    return 1

def dobivyvl(x,y,z):    # по y назад
    if (y - 1 < 0 or massive[x][y-1][z] > 0):
        return 0

    minx = maxx = x; miny = maxy = y; minz = maxz = z # запоминаем координаты
    # стреляем
    res = vistrel(x,y-1,z)
    if (res == 4):
        return 4
    if (res == 0):
        return 0
    miny -= 1
    if (res==1): # ранили
        #print "Ранили" # теперь не может быть несколько направлений, фиксируем x
        for ps in range(2): # не больше 4 палубника, а уже 2 подбили
            # по x назад
            if (miny - 1 < 0 or massive[x][miny-1][z] > 0):
                break
            res = vistrel(x,miny-1,z)
            if (res == 4):
                return 4
            if (res==0): # промазали, значит вперед, добиваем
                break
            miny -= 1
            if (res<>1): # ранили
                break
        if (res < 2): # еще не убили, значит вперед по x
            for ps in range(2): # не больше 4 палубника, а уже 2 подбили
                # по x вперед
                if (maxy + 1 > 9 or massive[x][maxy+1][z] > 0): # тупиковая ситуация с кораблем
                    print "ERRRROR2!!!"
                    break
                res = vistrel(x,maxy+1,z)
                if (res == 4):
                    return 4
                maxy += 1
                if (res<>1): # не ранили
                    break
    if (res <> 2):
        print "ERRRROR3!!!"
        return 0
        # подбили
    dlin = maxy-miny+1
    masko[dlin-1] -= 1
 #   print "Осталось толстушек(%i): %i" % (dlin, masko[dlin-1])
    for fds in range(miny, maxy+1):
        flagmas(x, fds,z)
    return 1

def dobivzvl(x,y,z):    # по y назад
    if (z - 1 < 0 or massive[x][y][z-1] > 0):
        return 0

    minx = maxx = x; miny = maxy = y; minz = maxz = z # запоминаем координаты
    # стреляем
    res = vistrel(x,y,z-1)
    if (res == 4):
        return 4
    if (res == 0):
        return 0
    minz -= 1
    if (res==1): # ранили
        #print "Ранили" # теперь не может быть несколько направлений, фиксируем x
        for ps in range(2): # не больше 4 палубника, а уже 2 подбили
            # по x назад
            if (minz - 1 < 0 or massive[x][y][minz-1] > 0):
                break
            res = vistrel(x,y,minz-1)
            if (res == 4):
                return 4
            if (res==0): # промазали, значит вперед, добиваем
                break
            minz -= 1
            if (res<>1): # ранили
                break
        if (res < 2): # еще не убили, значит вперед по x
            for ps in range(2): # не больше 4 палубника, а уже 2 подбили
                # по x вперед
                if (maxz + 1 > 9 or massive[x][y][maxz+1] > 0): # тупиковая ситуация с кораблем
                    print "ERRRROR2!!!"
                    break
                res = vistrel(x,y,maxz+1)
                if (res == 4):
                    return 4
                maxz += 1
                if (res<>1): # не ранили
                    break
    if (res <> 2):
        print "ERRRROR3!!!"
        return 0
        # подбили
    dlin = maxz-minz+1
    masko[dlin-1] -= 1
#    print "Осталось толстушек(%i): %i" % (dlin, masko[dlin-1])
    for fds in range(minz, maxz+1):
        flagmas(x, y, fds)
    return 1

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("fight.quals.ructf.org", 10000))

print s.recv(4096)
f=open("!qa", "w")
# Получаем карту
while 1:
    karta = s.recv(4096)
    print >>f, karta
    kors = karta.split("\n") # разделяем на координаты кораблей

    # Всего 50 кораблей
    # создаем массив
    masko = [20, 15, 10, 5]
    massive = zeros( (10,10,10) )
    # алгоритм по главной диагонале 4
    for i in range(4):
        for j in range(4):
            if i * 4 + j > 9:
                break
            for k in range(4):
                if i * 4 + j + k > 9:
                    break
                (x, y, z) = (i*4+j, i*4+j, i*4+j+k) # левая диагональ
                #print "massive ", (x,y,z), massive[x][y][z]
                if massive[x][y][z] > 0:
                    continue
                res = vistrel(x,y,z)
                if (res==1): # ранили
    #                print "Ранили" # теперь может быть несколько направлений
                    if (dobivxvl(x,y,z) > 0):
                        continue
                    if (dobivyvl(x,y,z) > 0):
                        continue
                    if (dobivzvl(x,y,z) > 0):
                        continue
                    if (dobivxvr(x,y,z) > 0):
                        continue
                    if (dobivyvr(x,y,z) > 0):
                        continue
                    if (dobivzvr(x,y,z) > 0):
                        continue

                if (res == 2): # подбили
                    masko[0] -= 1
   #                 print "Осталось однушек: %i" % masko[0]
                    flagmas(x,y,z)
    print "left ended", masko
    # алгоритм по обратной диагонале 4
    for i in range(4):
        for j in range(4):
            if i * 4 + (3-j) > 9:
                continue
            for k in range(4):
                if i * 4 + (3-j) + k > 9:
                    continue
                (x, y, z) = (i*4+(3-j), i*4+(3-j), i*4+(3-j)+k) # левая диагональ
                #print "massive ", (x,y,z), massive[x][y][z]
                if massive[x][y][z] > 0:
                    continue
                res = vistrel(x,y,z)
                if (res==1): # ранили
 #                   print "Ранили" # теперь может быть несколько направлений
                    if (dobivxvl(x,y,z) > 0):
                        continue
                    if (dobivyvl(x,y,z) > 0):
                        continue
                    if (dobivzvl(x,y,z) > 0):
                        continue
                    if (dobivxvr(x,y,z) > 0):
                        continue
                    if (dobivyvr(x,y,z) > 0):
                        continue
                    if (dobivzvr(x,y,z) > 0):
                        continue

                if (res == 2): # подбили
                    masko[0] -= 1
  #                  print "Осталось однушек: %i" % masko[0]
                    flagmas(x,y,z)
    print "right ended", masko
    # все остальное
    res=0
    for i in range(10):
        if (res==4):
            break
        for j in range(10):
            if (res==4):
                break
            for k in range(10):
                if (res==4):
                    break
                (x, y, z) = (i,j,k)
                #print "massive ", (x,y,z), massive[x][y][z]
                if massive[x][y][z] > 0:
                    continue
                res = vistrel(x,y,z)
                if (res==4):
                    break
                if (res==1): # ранили
 #                   print "Ранили" # теперь может быть несколько направлений
                    res = dobivxvl(x,y,z)
                    if (res > 0):
                        continue
                    res = dobivyvl(x,y,z)
                    if (res > 0):
                        continue
                    res = dobivzvl(x,y,z)
                    if (res > 0):
                        continue
                    res = dobivxvr(x,y,z)
                    if (res > 0):
                        continue
                    res = dobivyvr(x,y,z)
                    if (res > 0):
                        continue
                    res = dobivzvr(x,y,z)
                    if (res > 0):
                        continue

                if (res == 2): # подбили
                    masko[0] -= 1
#                    print "Осталось однушек: %i" % masko[0]
                    flagmas(x,y,z)
    print "ended", masko
    f.flush()
print >>f, s.recv(4096) # выводим на экран принятый ответ
