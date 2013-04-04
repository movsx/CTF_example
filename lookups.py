# -*- coding: utf-8 -*-
### Интересный пример скрипта, включающий подключение к серверу, многопоточность и запоминание правильных ответов для последующехо использования

### условие задачи
"""
    Robots enjoy some strange games and we just can’t quite figure this one out.
    Maybe you will have better luck than us.
    Title: The Game (100)
    Category: Potpourri
"""

### Мысли разработчика
"""
    The challenge consisted of a game we could play by connecting to a service running on port 6969.
    The game provided two hex strings, and our job was to find out which one was the biggest.
    To get the key, we had to win 75 runs in a row.

        $ nc ec2-23-21-19-72.compute-1.amazonaws.com 6969
        You have gotten 0 of 75
        Choice 1 = a5f1bec1c7078886e7e194f50c0ebd7580
        Choice 2 = f17775ea8c035349a2aca2a8bb3072897e
        Which one is bigger? (1 or 2)
        2
        Wrong <img src="http://eindbazen.net/wp-includes/images/smilies/icon_sad.gif" alt=":(" class="wp-smiley">

    --------------------
    Playing the game

    After playing for a while and trying to find a way to give the correct answer, we got stuck.
    We could win around 10 runs in a row, but never came close to 75…

    Luckily, one of our team members suggested that those numbers might be reused.
    If so, we could create some kind of cache mechanism, and find the answer by checking the previous results.
    Because the service provided the answer for each try, this seemed plausible, and we immediately started dumping the numbers to a file.
    Caching the numbers

    We discovered that the numbers were indeed reoccurring (it appeared that a total of ~500 numbers were used), so this approach seemed to be the right way to go.

    Now we only had to relate the numbers to each other and answer to the service based on the results we found earlier.
    To do this, we wrote the following python script:

"""

import socket, re, threading, time

hashes = []
lookup = []
running = True
highscore = 0
requests = 0

def add(high, low):
    if not lookup:
        lookup.append(low)
        lookup.append(high)
    hashes.append([high,low])

def update():
    while running:
        for n1, n2 in hashes:
            if not n1 in lookup and not n2 in lookup:
                continue
            if n1 in lookup and n2 in lookup:
                index1 = lookup.index(n1)
                index2 = lookup.index(n2)
                if index1 < index2:
                    lookup[index1], lookup[index2] = lookup[index2], lookup[index1]
            else:
                if n1 in lookup:
                    lookup.insert(lookup.index(n1), n2)
                else:
                    lookup.insert(lookup.index(n2), n1)
        time.sleep(1)

def get_answer(n1, n2):
    if n1 in lookup and n2 in lookup:
        return "1" if lookup.index(n1) > lookup.index(n2) else "2"
    else:
        return "1"

def play():
    global running, highscore, requests

    s = socket.create_connection(('ec2-23-21-19-72.compute-1.amazonaws.com', 6969))
    fs = s.makefile()

    while (running):
        score = re.match("You have gotten ([0-9]+) of 75", fs.readline()).group(1)
        choice1 = re.match("Choice 1 = (.*)", fs.readline()).group(1)
        choice2 = re.match("Choice 2 = (.*)", fs.readline()).group(1)
        if int(score) > int(highscore):
            highscore = score
            print "Highscore: %s" % score

        fs.readline()
        answer = get_answer(choice1, choice2)
        s.send(answer + "\n")
        fs.readline()

        correct = fs.readline() == "Correct!\n"
        fs.readline()

        if correct and score == "74":
            running = False
            print s.recv(1024)
            print "Number of requests: %d" % requests
        elif (correct and answer == "1") or (not correct and answer == "2"):
            add(choice1, choice2)
        else:
            add(choice2, choice1)

        requests += 1

threading.Thread(target=update).start()
for i in range(50):
    threading.Thread(target=play).start()

### Мысли
"""
    The script keeps track of all combinations received in the variable hashes.
    Each element contains two values (n1 and n2) where the first value (n1) is the highest number.

    Initially, the first two hashes are added to the list lookup.
    Each second, the lookup list is updated based on the following conditions:

        If both n1 and n2 do not exist in lookup, do nothing
        If only n1 exists in lookup: insert n2 just before n1
        If only n2 exists in lookup: insert n1 just after n2
        If both n1 and n2 exist in lookup, but n1 < n2, swap n1 for n2

    This way, the lookup table is filled and sorted based on the results found.
    To get an answer for the next question, we check which of the numbers has the highest index in the list lookup

    By using 50 threads we could fetch the key in less than 30 seconds:

        # ./game.py
        Yay you have won!
        The key is: d03snt_3v3ry0n3_md5

        Number of requests made: 5859

        real    0m28.983s
        user    0m9.765s
        sys     0m0.468s
"""
