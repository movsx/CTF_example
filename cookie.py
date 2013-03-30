# -*- coding: utf-8 -*-
from mechanize import Browser

br = Browser()
# часть кода, выполняющая GET запрос с куками к ctftime.org
br.open("https://ctftime.org/") # fake'вый вызов открытия странички
br.set_cookie("csrftoken=EB6XXXXXXXXXXXXXXXXXXXXXXXXXXpAC")
br.set_cookie("sessionid=e56XXXXXXXXXXXXXXXXXXXXXXXXXXfc6") # пример куков для ctftime
br.set_handle_equiv(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)
br.open("https://ctftime.org/")
print >>open('test.txt','w+'), br.response().read() # вывод в файл полученного ответа

# Часть кода, выполяющая обход ТЕКСТОВОЙ капчи
br.open('http://ctf.nullcon.net/challenges/programming/challenge.php')
text = br.response().read().split("\n") # получили ответ и разбили по строкам
string=text[4].replace("<span>","").replace("</span>","").replace("&nbsp;", " ").replace("</p>","").strip() # вместо подготовки регулярного выражения dummy убираем лишние фиксированные символы с 5 строки
br.select_form(nr=0) # находим первую форму на страничке
br.method='POST' # настраиваем метод POST
br['answer'] = string # подставляем в поле answer полученный результат
print br.submit().read() # отправляем форму на сервер и печатаем полученный результат

