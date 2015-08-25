#!/usr/bin/python

from __future__ import print_function
from itertools import *

#data is like (value, row, col)
class CONSTRAINT:
    def __init__(self, N):
        self.N = N
   
    def trow_constraints(self):
        return self.N 

    def tcol_constraints(self):
        return self.N
    #remove the corner boxes which have only 1 diagnol
    def tldiag_constraints(self):
        return 2*self.N - 1 - 2

    #remove the corner boxes which have only 1 diagnol
    def trdiag_constraints(self):
        return 2*self.N - 1 - 2

    # queen in a row
    # (1,  1), (1,  2), (1,  3) ... (1, N) = 1.. N
    # total N constraints
    def row_constraint(self, d):
        (r, c) = d
        return r

    #similarly for column
    #total N constraints
    def col_constraint(self, d):
        (r, c) = d
        return c

    # this is just a observation
    # do no include the diagnols with one element
    def ldiag_constraint(self, d):
        (r, c) = d
        return ((r + c) - 1) - 1

    # this is just a observation
    # do no include the diagnols with one element
    def rdiag_constraint(self, d):
        (r, c) = d
        return (self.N - (r - c)) - 1


    def generate(self, d, result):
        trow  = self.trow_constraints()
        tcol  = self.tcol_constraints()
        tldiag = self.tldiag_constraints()
        trdiag = self.trdiag_constraints()

        display = False
        if len(d) > 0:
            display = True
        else:
            print (self.N * self.N, trow + tcol + tldiag + trdiag, self.N + self.N)


        ind = 0
        l = [i+1 for i in range(self.N)]
        for k, v in enumerate(product(l, l)):
            r, c = v
            if display:
                if ind < len(d) and d[ind] == k+1:
                    print (r, "in", (r, c))
                    result.append([r,c])
                    ind += 1
            else:
                if (r == N and c == 1) or (r == 1 and c == N):  # dont print rdiag
                    print(self.row_constraint(v), 
                            trow + self.col_constraint(v), 
                            trow + tcol + trdiag + self.ldiag_constraint(v))
                elif (r == 1 and c == 1) or (r == N and c == N): # dont print ldiag
                    print(self.row_constraint(v), 
                            trow + self.col_constraint(v), 
                            trow + tcol + self.rdiag_constraint(v))
                else:  
                    print(self.row_constraint(v), 
                            trow + self.col_constraint(v), 
                            trow + tcol + self.rdiag_constraint(v), 
                            trow + tcol + trdiag + self.ldiag_constraint(v))

    def generate_constraint(self):
        self.generate([], [])

    def interpret_result(self, l):
        result = []
        l.sort()
        self.generate(l, result)
        self.draw(result)


    def draw(self, result):
        for i in range(self.N):        
            print ("+---" * self.N, end = '')
            print("+")
            for j in range(1, self.N+1):
                if result[i][1] == j:
                    print("| Q ", end= '') 
                else:
                    print("|   ", end='') 
            print("|")
        print("+---" * self.N, end = '')
        print("+")


N = int(raw_input("Enter the size of grid in N: "))
c = CONSTRAINT(N)
#c.generate_constraint()

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
