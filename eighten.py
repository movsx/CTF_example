# -*- coding: utf-8 -*-
### Решение игры в 8-нашки (аналог пятнашек)
# ключевая особенность: Нужно решение вводить ОДНОЙ строкой, иначе штраф за длительный ответ
import sys
from optparse import OptionParser
import math
from struct import pack
import heapq

class Solver:
    def __init__(self, n):
        self.N = n
        self.L = n * n

        self.GOAL = range(1, self.L)
        self.GOAL.append(0)

        # slide rules
        self.SR = {}
        for i in range(self.L):
            s = []
            if i - self.N >= 0:
                s.append(i - self.N)
            if (i % self.N) - 1 >= 0:
                s.append(i - 1)
            if (i % self.N) + 1 < self.N:
                s.append(i + 1)
            if i + self.N < self.L:
                s.append(i + self.N)
            self.SR[i] = s

        # queue
        self.queue = []
        self.enqueued = {}

        # verbose
        #self.verbose = 104999
        self.verbose = 8963

        # h
        self.w = 1
        self.h = self.heuristics

    def is_solvable(self, tiles):
        x = 0
        for p in range(len(tiles)):
            a = tiles[p]
            if a < 2 :
                continue
            for b in tiles[p:]:
                if b == 0:
                    continue
                if a > b:
                    x = x + 1
        return (x & 1) == 0

    def neighbors(self, tiles):
        n = []
        a = tiles.index(0)
        for b in self.SR[a]:
            n.append(self.swap(list(tiles), a, b))
        return n

    def swap(self, tiles, a, b):
        tiles[a], tiles[b] = tiles[b], tiles[a]
        return tiles

    def display(self, tiles):
        for i in range(self.L):
            if tiles[i]:
                print '%(n)#2d' % {'n': tiles[i]},
            else:
                print '  ',
            if i % self.N == self.N - 1:
                print

    def enqueue(self, state):
        (tiles, parent, h, g) = state

        if self.verbose > 0 and len(self.enqueued) % self.verbose == self.verbose - 1:
            print " -->", len(self.enqueued), g

        f = h * self.w + g;
        heapq.heappush(self.queue, (f, state))

    def dequeue(self):
        if len(self.queue) <= 0:
            return None
        (f, state) = heapq.heappop(self.queue)
        return state

    def heuristics(self, tiles):
        return 0;

    def manhattan(self, tiles):
        h = 0
        for i in range(self.L):
            n = tiles[i]
            if n == 0:
                continue
            h += int(abs(n - 1 - i) / self.N) + (abs(n - 1 - i) % self.N)
        return h

    def hamming(self, tiles):
        h = 0
        for i in range(self.L):
            n = tiles[i]
            if n > 0 and n - 1 != i:
                h += 1
        return h

    def solve(self, initial):
        if not self.is_solvable(initial):
            return None

        state = (initial, None, self.h(initial), 0);
        if initial == self.GOAL:
            return state

        self.enqueue(state)

        while True:
            state = self.dequeue()
            if (not state):
                break

            (tiles, parent, h, g) = state
            neighbors = self.neighbors(tiles)
            for n_tiles in neighbors:
                if n_tiles == self.GOAL:
                    return (n_tiles, state, 0, g + 1)

                packed = pack(self.L*'B', *n_tiles)
                if (packed in self.enqueued):
                    continue;
                self.enqueued[packed] = True

                n_state = (n_tiles, state, self.h(n_tiles), g + 1)
                self.enqueue(n_state)

def parseboard(s): # делаем массив из картинки
    data = s.recv(1024)
    arrlines = data.split("\n") # разбиваем массив на строки (интересны 3, 8, 13 строки)
    ini = []
    colpos = [3, 9 ,15]
    rowpos = [3, 8, 13]
    for i in range (9):
        row = rowpos[i / 3]
        col = colpos[i % 3]
        ini.append(int(arrlines[row][col].replace(' ', '0')))
    return ini

def senddir(s, delta):
    char = ""
    if delta == -1:
        char = "l"
    if delta == -3:
        char = "u"
    if delta == 1:
        char = "r"
    if delta == 3:
        char = "d"
    return char

def main(options, args):
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect(('pieceofeight2.shallweplayaga.me', 8273))
    except socket.error:
        print "socket connection failed"
        exit()
    z = 0
    while (1):
        z += 1; print z
        initial = parseboard(s)
        solver = Solver(int(math.sqrt(len(initial))))

        solver.verbose = 0#int(options.verbose)
        solver.w = float(options.weight)
        solver.h = solver.manhattan
        #if int(options.function) == 1:
        #    solver.h = solver.hamming
        #elif int(options.function) == 2:
        #    solver.h = solver.manhattan

        state = solver.solve(initial)
        if not state:
            print "No solution possible"
            return 1

        solution = []
        while state:
            (tiles, parent, h, g) = state
            solution.insert(0, tiles)
            state = parent

        n = 0
        pts = tiles.index(0)
        qts = ""
        for tiles in solution:
            qts += senddir(s, pts-tiles.index(0))
            pts = tiles.index(0)
            #solver.display(tiles)
            n += 1
        s.send(qts+"\n")
        while (1):
            q = s.recv(10240)
            if "key" in q:
                break
        s.send("1")
        print "Number of states enqueued =", len(solver.enqueued)
    return 0

if __name__ == '__main__':
    parser = OptionParser(usage="usage: %prog [options] [tile] [tile] [tiles ...]")
    parser.add_option("-v", "--verbose", metavar="<level>",
                      default=8963)
    parser.add_option("-f", "--function", metavar="<fid>",
                      help="heuristics function. 1 for hamming, 2 for manhattan [default: None as breadth first]",
                      default=0)
    parser.add_option("-w", "--weight", metavar="<n>",
                      help="weighting of the heuristics function [default: 1]",
                      default=1)
    (options, args) = parser.parse_args()

    sys.exit(main(options, args))

