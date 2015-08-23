#!/usr/bin/python

from itertools import *
#data is like (value, row, col)

class CONSTRAINT:
    def __init__(self, N):
        self.N = N
   
    def trow_constraints(self):
        return self.N 

    def tcol_constraints(self):
        return self.N

    def tldiag_constraints(self):
        return 2*self.N - 1

    def trdiag_constraints(self):
        return 2*self.N - 1

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
    def ldiag_constraint(self, d):
        (r, c) = d
        return ((r + c) - 1)

    # this is just a observation
    def rdiag_constraint(self, d):
        (r, c) = d
        return (self.N - (r - c))


    def generate(self, r):
        trow  = c.trow_constraints()
        tcol  = c.tcol_constraints()
        tldiag = c.tldiag_constraints()
        trdiag = c.trdiag_constraints()

        display = False
        if len(r) > 0:
            display = True
        else:
            print self.N * self.N, trow + tcol + tldiag + trdiag


        ind = 0
        l = [i+1 for i in range(self.N)]
        for k, v in enumerate(product(l, l)):
            if display:
                if ind < len(r) and r[ind] == k+1:
                    print v[0], "in", (v[0], v[1])
                    ind += 1
            else:
                print c.row_constraint(v), trow + c.col_constraint(v), trow + tcol + c.rdiag_constraint(v), trow + tcol + trdiag + c.ldiag_constraint(v)

    def generate_constraint(self):
        self.generate([])

    def interpret_result(self, l):
        l.sort()
        print l
        self.generate(l)

N = int(raw_input())
c = CONSTRAINT(N)
c.generate_constraint()

inp = raw_input("Want to interpret results?")
if inp == "yes":
    l = map(int, raw_input("enter the result: ").strip().split())
    c.interpret_result(l)
