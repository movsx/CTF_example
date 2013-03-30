# -*- coding: utf-8 -*-
from mechanize import Browser

br = Browser()
br.open("https://ctftime.org/") # fake'вый вызов открытия странички
br.set_cookie("csrftoken=EB6XXXXXXXXXXXXXXXXXXXXXXXXXXpAC")
br.set_cookie("sessionid=e56XXXXXXXXXXXXXXXXXXXXXXXXXXfc6") # пример куков для ctftime
br.set_handle_equiv(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)
br.open("https://ctftime.org/")
print >>open('test.txt','w+'), br.response().read() # вывод в файл полученного ответа


