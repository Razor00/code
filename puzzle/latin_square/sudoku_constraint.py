#!/usr/bin/python

from __future__ import print_function
from itertools import *
import math

#data is like (value, row, col)
class CONSTRAINT:
    def __init__(self, N):
        self.N = N
        self.boxN = math.sqrt(N)
        self.boxS = N
  
    def tcell_constraints(self):
        return self.N * self.N

    def trow_constraints(self):
        return self.N * self.N

    def tcol_constraints(self):
        return self.N * self.N

    def tbox_constraints(self):
        return self.N * self.N

    def cell_constraint(self, d):
        (r, c, v) = d
        return self.N * (r-1) + c

    def row_constraint(self, d):
        (r, c, v) = d
        return self.N * (r-1) + v

    def col_constraint(self, d):
        (r, c, v) = d
        return self.N * (c-1) + v

    def box_constraint(self, d):
        (r, c, v) = d
        brow  = math.ceil(r/self.boxN)
        bcol  = math.ceil(c/self.boxN)
        bnum  = self.boxN * (brow - 1) + bcol
        return int(self.boxS * (bnum - 1) + v)

    def possibilities(self):
        return self.N * self.N * self.N

    def total_constraints(self):
        return    self.tcell_constraints() + self.trow_constraints() + self.tcol_constraints() + self.tbox_constraints()

    def generate(self, d, result):

        tcell = self.tcell_constraints()
        trow  = self.trow_constraints()
        tcol  = self.tcol_constraints()
        tbox  = self.tbox_constraints()

        display = False
        if len(d) > 0:
            display = True
        else:
            print (self.possibilities(), self.total_constraints(), self.total_constraints())


        ind = 0
        l = [i+1 for i in range(self.N)]
        for k, t  in enumerate(product(l, l, l)):
            r, c, v = t
            if display:
                if ind < len(d) and d[ind] == k+1:
                    print (v, "in", (r, c))
                    result.append(t)
                    ind += 1
            else:
                    print(self.cell_constraint(t),  
                    tcell + self.row_constraint(t), 
                    tcell + trow  + self.col_constraint(t),
                    tcell + trow  + tcol +  self.box_constraint(t))

    
    def generate_constraint(self):
        self.generate([], [])

    def interpret_result(self, l):
        result = []
        l.sort()
        self.generate(l, result)
        if self.check(result):
            print ("Valid solution")
            self.draw(result)
        else:
            print ("InValid solution")

    def check_rc(self, l, pos):
        for i in range(1, self.N+1):
            if l[pos].count(i) != 1:
                print(l[pos])
                return False
        return True
    
    def check(self, result):
           
        s = [[0 for i in range(self.N+1)] for j in range(self.N+1)] 
        r = [[0 for i in range(self.N+1)] for j in range(self.N+1)] 
        k = 0
        for i in range(1, self.N+1):
            for j in range(1, self.N+1):
                s[j][i] = r[i][j] = result[k][2]
                k += 1

        
        for i in range(1, self.N+1):
            if not (self.check_rc(r, i) and self.check_rc(s, i)):
                return False
        return True

    def draw(self, result):
        sorted(result, key = lambda x : (x[0], -x[1])) 
        k = 0
        for i in range(1, self.N+1):        
            print ("+----" * self.N, end = '')
            print("+")
            for j in range(1, self.N+1):
                print("| %2d " % result[k][2], end= '') 
                k += 1
            print("|")
        print("+----" * self.N, end = '')
        print("+")


N = int(raw_input("Enter the size of grid in N: "))

sN = math.sqrt(N)
if sN * sN != N:
    print ("N is not a square number")
    exit(0)

c = CONSTRAINT(N)

inp = raw_input("Want to interpret results?")
if inp == "yes":
    while True:
        l = map(int, raw_input("enter the result: ").strip().split())
        if len(l) != 0:
            c.interpret_result(l)
        else:
            break
else:
    c.generate_constraint()
