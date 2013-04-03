# -*- coding: utf-8 -*-
import random

### Функции проверки простых чисел

########################################################
# Теорема Ферма. Работает медленно
def primFerma(a,n):
    if a**(n-1)%n==1:
        return True
    else:
        return False

########################################################
# Первый вариант теста. Не отработал на первых трех числах. Не понравился.
def toBinary(n):
    r = []
    while (n > 0):
        r.append(n % 2)
        n = n / 2
        return r

def MillerRabin(n, s = 1):
    for j in xrange(1, s + 1):
        a = random.randint(1, n - 1)
        b = toBinary(n - 1)
        d = 1
        for i in xrange(len(b) - 1, -1, -1):
            x = d
            d = (d * d) % n
            if d == 1 and x != 1 and x != n - 1:
                return False # sost
            if b[i] == 1:
                d = (d * a) % n
                if d != 1:
                    return False # sost
                return True # prime

########################################################
# Тест Миллера-Рабина (вариант 2)
def miller_rabin_pass(a, s, d, n):
    a_to_power = pow(a, d, n)
    if a_to_power == 1:
        return True
    for i in xrange(s-1):
        if a_to_power == n - 1:
            return True
        a_to_power = (a_to_power * a_to_power) % n
    return a_to_power == n - 1

def miller_rabin(n):
    d = n - 1
    s = 0
    while d % 2 == 0:
        d >>= 1
        s += 1
    for repeat in xrange(20):
        a = 0
        while a == 0:
            a = random.randrange(n)
        if not miller_rabin_pass(a, s, d, n):
            return False
    return True

########################################################
# Тест Миллера-Рабина (вариант 3, вроде пошустрее всех)
def millerTest(a, i, n):
    global pools
    if i == 0:
        pools -= 1
        return 1
    pools += 1
    if pools > 50: # Искусственное ограничение, чтобы не было переполнения рекурсии
        pools -= 1
        return 1
    x = millerTest(a, i / 2, n)
    if x == 0:
        pools -= 1
        return 0
    y = (x * x) % n
    if ((y == 1) and (x != 1) and (x != (n - 1))):
        pools -= 1
        return 0
    if (i % 2) != 0:
        y = (a * y) % n
    pools -= 1
    return y

def is_prime(x):
    for i in primes:
        if i >= x:
            break
        if x % i == 0:
            return False
    if (int(x**1/2)*int(x**1/2) == x):
        return False
    if x < 10:
        return True
    if millerTest(random.randint(2, x - 2), x - 1, x) == 1:
        return True
    else:
        return False

### функция поиска простых чисел по дурацкой последовательности в двоичном виде
# Для ускорения процесса используем таблицу простых чисел до 166000
# Ссылка на таблицу http://dl.dropbox.com/u/17463542/prime2.txt
def durnoj_prim():
    primes=open("prime2.txt",'r').read() # таблица простых чисел
    primes=primes.split()
    count=0 # порядковый номер
    for i in range(len(primes)):
        primes[i]=int(primes[i])
    s=""
    pools = 0
    for i in range(len(primes)):
        s+=bin(primes[i])[2:]
        x=int(s,2)
        pools = 0
        if is_prime(x):
            count+=1
            print(count,x)

primes=[]
pools = 0 # уровень рекурсии текущий
print is_prime(13750)
