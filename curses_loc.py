# -*- coding: utf-8 -*-
import curses
import locale
# Для корректной работы curser под ОС Windows необходимо установить дополнительные пакеты с адреса http://www.lfd.uci.edu/~gohlke/pythonlibs/#curses
def Main():
    # для корректного отображения русского языка
    locale.setlocale(locale.LC_ALL, '')

    # инициализация
    stdscr = curses.initscr()

    # смотрим можно ли менять цвета
    has_color = curses.has_colors()

    if has_color:
        # старт работы с цветами
        curses.start_color()

        # добавляем новую пару цветов
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
        # установим новую пару цветов по умолчанию
        stdscr.attrset(curses.color_pair(1))

        # установим цвет фона
        stdscr.bkgdset(ord(' '), curses.color_pair(1))
        # очищаем экран, чтобы цвет фона применился
        stdscr.clear()

    # разрешаем использовать стрелки и тд
    stdscr.keypad(1)

    # убираем курсор
    curses.curs_set(0)

    # рисуем стильную рамочку
    stdscr.border(0)

    # вывод текста
    stdscr.addstr(12, 25, "Python curses в действии!")
    stdscr.addstr(13, 25, "Enter parameter: ")

    # обновление экрана
    stdscr.refresh()

    # читаем символ
    x = stdscr.getch()
    stdscr.clear()
    stdscr.border(0)

    if x == ord('1'):
        stdscr.addstr(12, 25, "Hello world!")
        stdscr.getch()
    if x == ord('2'):
        stdscr.addstr(12, 25, "Alloha Havaii!")
        stdscr.getch()
    if x == curses.KEY_LEFT:
        stdscr.addstr(12, 25, "KEY_LEFT")
        stdscr.getch()

    stdscr.keypad(0)
    curses.curs_set(1)
    curses.endwin()

Main()