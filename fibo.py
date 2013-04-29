# -*- coding: utf-8 -*-
# функция вычисления n-го числа Фибоначи, суммы всех чисел Фибоначи до N, и суммы всех четных чисел и суммы всех нечетных
# работает неоптимизированно, так как на самом деле можно считать только последние числа, но лень додумать
def fib(n):
    a, b = 0, 1 # у некоторых буржуев есть точка зрения, что начинать надо с 1,1
    sum = sum_ord = sum_noord = 0
    for i in range(n-1):
        a, b = b, a + b
        if i % 2 == 0:
            sum_ord += a # сумма четных элементов
        else:
            sum_noord += a # сумма нечетных элементов
        sum += a # общая сумма элементов
    print "fib_sum_x:"+str(sum)
    print "fib_sum_ord_x:"+str(sum_ord)
    print "fib_sum_noord_x:"+str(sum_noord)
    return a

print "fib:"+str(fib(8))

#более быстрый алгоритм
def fastfib(n):
    import math
    return round(((1+math.sqrt(5))/2)**n/(math.sqrt(5)))
