# -*- coding: utf-8 -*-
# __author__ = 'movsx'
import string, base64, hashlib
### Решение задачи с польской записью
# сам пример достаточно вырожденный, так как внутри еще использовался язык whitespace
# решить правильно не смогли, но код решили оставить на всякий случай
# отличие от основной польской записи в том, что есть стек (память) для временного хранения чисел
# максимально использовалось две ячейки
def summ(a,b):
    return a+b
def sub(a,b):
    return abs(b-a)
def mul(a,b):
    return a*b
def div(a,b):
    return b/a

def calcExpression(exp):
    stack = [] # Стек для хранения операций
    mem = [0,0] # внутренняя память, используется для операций типа <, >
    prin = prin2 = "" # строка для вывода на печать
    #объявляем словарь с функциями
    funcs = {'+':summ,'-':sub,'*':mul,'/':div}
    # массив вывода whitespace
    wh_print = open("ws_print.txt").readlines()
    count_n = 0;
    for i in range(len(exp)):
        c = exp[i]
        x = 0
        if c == '\n':
            if count_n > 112:
                continue
            if count_n % 2 > 0: # print whitespace
                #prin = prin + "%02x" % int(wh_print[count_n // 2].strip()) # берем из массива печати whitespace
                prin = prin + chr(int(wh_print[count_n // 2].strip())) # берем из массива печати whitespace
            count_n += 1
            continue
        if c in ['\t',' ']:
            continue
        if c in ['+','-','/','*']:
            #достать два последних числа из стека
            a = stack.pop()
            b = stack.pop()
            #выполнить операцию по ключу С
            x = funcs[c](a,b)
            #print a, b, c, x # debug'овый вывод
            stack.append(x) # результат вернуть обратно в стек
        else:
            if c == '>': # на вершине стека у нас адрес ячейки памяти, куда положить
                a = stack.pop()
                b = stack.pop()
                mem[a] = b
                continue
            if c == '<': # извлечь из памяти в стек значение
                a = stack.pop()
                stack.append(mem[a])
                continue
            if c == "P": # вывести на экран. Не понятен формат вывода
                temp = stack.pop()
                #prin = prin + "%02x" % temp # незначащие нули не добавляем
                prin = prin + chr(temp) # незначащие нули не добавляем
                #if (temp < 256): # Может вывод должен быть в символьном формате
                #    print chr(temp)
                continue
            # вариант 1, когда могут быть двузначные числа. Вариант дурацкий по коду, не работает из-за нехватки стека
            #ptsfake = exp[i:].replace(" ","\t").replace("\n","\t").replace("+","\t").replace("-","\t").replace("/","\t").replace("*","\t").replace("<","\t").replace(">","\t").split("\t")[0]
            #x = int(ptsfake)
            #print x, ptsfake
            #if x > 9:
            #    exp = exp[:i+1] + exp[i+2:]
            # вариант 2. Только однозначные числа
            x = int(c)
            stack.append(x)

    print prin
    m = hashlib.md5()
    m.update(prin+prin2)
    print m.hexdigest()
    m1 = hashlib.md5()
    m1.update(prin2+prin)
    print m1.hexdigest()
    print base64.b64encode(prin+prin2)
    print base64.b64encode(prin2+prin)
    #print stack #debug
    #print len(stack) #debug
    return x

str = open("txt.txt", "r").read()
calcExpression(str)