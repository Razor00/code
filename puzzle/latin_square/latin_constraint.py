#!/usr/bin/python

from __future__ import print_function
from itertools import *
import math

#data is like (value, row, col)

class CONSTRAINT:
    def __init__(self, N):
        self.N = N
# some number in 
# (1,  1), (1,  2), (1,  3) ... (1, N) = 1.. N
# (2,  1), (2,  2), (2,  3) ... (2, N) = N + 1...N
# (N-1,1), (N-1,2), (N-1,3) ... (N, N) = (N-1)N + 1... N
# total N*N constraints
   
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
    
    def cell_constraint(self, d):
        (r, c, v) = d
        return (r-1) * self.N + c


    def row_constraint(self, d):
        (r, c, v) = d
        return (v-1) * self.N + r

#similarly for column
#total N*N constraints

    def col_constraint(self, d):
        (r, c, v) = d
        return (v-1) * self.N + c

    def generate(self, d, result):
        display = False
        if len(d) > 0:
            display = True
        else:
            print (self.N * self.N * self.N, 3 * self.N * self.N, 3 * self.N * self.N, 0)

        tcell = self.total_cell_constraints()
        trow  = self.total_row_constraints()
        tcol  = self.total_col_constraints()
        ind = 0
        l = [i+1 for i in range(self.N)]
        for k, t in enumerate(product(l, l, l)):
            (r, c, v) = t
            if display:
                if ind < len(d) and d[ind] == k+1:
                    print (v, "in", (r, c))
                    result.append(t)
                    ind += 1
            else:
                print (self.cell_constraint(t), tcell + self.row_constraint(t), tcell + trow + self.col_constraint(t))

    def generate_constraint(self):
        self.generate([], [])

    def interpret_result(self, l):
        l.sort()
        result = [] 
        self.generate(l, result)
        if self.check(result):
            print ("Valid solution")
            self.draw(result)
        else:
            print ("InValid solution")

    def check_rc(self, l, pos):

        for i in range(1, self.N+1):
            if l[pos].count(i) != 1:
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
        # check box constraints

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


N = int(raw_input("Enter size of grid: "))
c = CONSTRAINT(N)
c.generate_constraint()

while True:
    inp = raw_input("Want to interpret results?")
    if inp == "yes":
        l = map(int, raw_input("enter the result: ").strip().split())
        c.interpret_result(l)
    else:
        break
