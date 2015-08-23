#!/usr/bin/python

from itertools import *
#data is like (value, row, col)

class CONSTRAINT:
    def __init__(self, N):
        self.N = N
# some number in 
# (1,  1), (1,  2), (1,  3) ... (1, N) = 1.. N
# (2,  1), (2,  2), (2,  3) ... (2, N) = N + 1...N
# (N-1,1), (N-1,2), (N-1,3) ... (N, N) = (N-1)N + 1... N
# total N*N constraints
   
    def cell_constraint(self, d):
        v, r, c = d
        return (r-1) * self.N + c

    def total_cell_constraints(self):
        return self.N * self.N

    def total_row_constraints(self):
        return self.N * self.N

    def total_col_constraints(self):
        return self.N * self.N
# 1 at row 1, 2, 3, 4, 5, .. N would be first
# 2 at row 1, 2, 3, 4, 5. ,,,N would be next
# so 1.....N would be for 1
# N+1, N+2, ... , 2N for 2
# and so on
# total N*N constraints
    def row_constraint(self, d):
        (v, r, c) = d
        return (v-1) * self.N + r

#similarly for column
#total N*N constraints

    def col_constraint(self, d):
        (v, r, c) = d
        return (v-1) * self.N + c

    def generate(self, r):
        if len(r) > 0:

        print self.N * self.N * self.N, 3 * self.N * self.N
        tcell = c.total_cell_constraints()
        trow  = c.total_row_constraints()
        tcol  = c.total_col_constraints()
        ind = 0
        l = [i+1 for i in range(self.N)]
        for k, v in enumerate(product(l , l, l)):
            if len(r) > 0:
                if ind < len(r) and r[ind] == k+1:
                    print v[0], "in", (v[1], v[2])
                    ind += 1
            else:
                print c.cell_constraint(v), tcell + c.row_constraint(v), tcell + trow + c.col_constraint(v)

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
