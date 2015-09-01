#!/usr/bin/python

from __future__ import print_function
from itertools import *
import math
import os, sys, subprocess, signal

def signal_handler(signal, frame):
    sys.exit(0)

#data is like (value, row, col)
class CONSTRAINT:
    def __init__(self, N, path):
        self.N = N
        self.boxN = int(math.sqrt(N))
        self.boxS = N
        self.psols = []
        check = path.split("/")
        if path[0] != "/":
            path = os.getcwd() + "/" + path
        self.path = "/".join(path.split("/")[:-1])
  
    def tcell_constraints(self):
        return self.N * self.N

    def trow_constraints(self):
        return self.N * self.N

    def tcol_constraints(self):
        return self.N * self.N

    def tbox_constraints(self):
        return self.N * self.N

    def partial_solutions(self):
        return len(self.psols)

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
        brow  = math.ceil(r*1.0/self.boxN)
        bcol  = math.ceil(c*1.0/self.boxN)
        bnum  = self.boxN * (brow - 1) + bcol
        return int(self.boxS * (bnum - 1) + v)

    def possibilities(self):
        return self.N * self.N * self.N

    def total_constraints(self):
        return (self.tcell_constraints() +
                self.trow_constraints() + 
                self.tcol_constraints() + 
                self.tbox_constraints())


    def generate(self, d, result):

        tcell = self.tcell_constraints()
        trow  = self.trow_constraints()
        tcol  = self.tcol_constraints()
        tbox  = self.tbox_constraints()

        display = False
        if len(d) > 0:
            display = True
        else:
            print  (self.possibilities(), 
                    self.total_constraints(), 
                    self.total_constraints(), 
                    self.partial_solutions())


        ind = 0
        l = [i+1 for i in range(self.N)]
        for k, t  in enumerate(product(l, l, l)):
            (r, c, v) = t
            if display:
                if ind < len(d) and d[ind] == k+1:
                    #print (v, "in", (r, c))
                    result.append(t)
                    ind += 1
            else:
                    print  (self.cell_constraint(t),  
                            tcell + self.row_constraint(t), 
                            tcell + trow  + self.col_constraint(t),
                            tcell + trow  + tcol +  self.box_constraint(t))
        if not display:
            for p in self.psols:
                print(p)

    def generate_constraint(self):
        self.generate([], [])

    def check_row(self, l, pos):
        return self.check_list(l[pos])

    def check_col(self, l, pos):
        return self.check_list(l[pos])

    def check_box(self, l):
        return self.check_list(l)


    def check(self, result):
        r = [[0 for i in range(self.N+1)] for j in range(self.N+1)] 
        c = [[0 for i in range(self.N+1)] for j in range(self.N+1)] 
        k = 0
        for i in range(1, self.N+1):
            for j in range(1, self.N+1):
                c[j][i] = r[i][j] = result[k][2]
                k += 1

        
        for i in range(1, self.N+1):
            if not (self.check_row(r, i) and self.check_col(c, i)):
                return False
        # check box constraints
        # generate boxes sqrt(N) by sqrt(N) of N boxes
        # box (i, j): start row, start col
        br = 1
        bc = 1
        bsize = int(math.sqrt(self.N))
        for bnum in range(1, self.N+1):
            br = int(math.ceil(bnum*1.0/bsize)) 
            bc = bnum - (br-1) * bsize
            ar  = (br-1) * bsize + 1
            ac  = (bc-1) * bsize + 1
            l = [0] * self.N
            p = 0
            for i in range(bsize):
                for j  in range(bsize):
                    l[p] = r[ar + i][ac+j] 
                    p += 1
            if not self.check_box(l):
                return False
        return True

    def output(self, result):
        return [k for i,j,k in result]
                    
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

    def process(self, inp):
        for i,v in enumerate(inp):
            if v != 0:
                self.psols.append((i*self.N)+v)

    def reset(self):
        self.psols = []

    def generate_result(self, l, ret_list = False):
        result = []
        l.sort()
        self.generate(l, result)
        if self.check(result):
            print ("Valid solution")
            if ret_list:
                return self.output(result)
            else:
                self.draw(result)

        else:
            print ("InValid solution")

    def check_list(self, l):
        for i in range(1, self.N+1):
            if l.count(i) != 1:
                return False

        return True


def interpret_results(c):
    while True:
        l = map(int, raw_input("enter the result: ").strip().split())
        if len(l) == 0:
            break;
        c.generate_result(l)

def execute_n_interpret(c, inp_list, ask, ret_list = False):
    rescount = 1
    if inp_list:
        c.process(inp_list)

    ifile = "/tmp/sudoku_" + str(c.N) + ".txt" 
    old = sys.stdout
    sys.stdout = open(ifile, "w")

    c.generate_constraint()
    
    sys.stdout.close()
    sys.stdout = old
  
    classpath = c.path + ":" + c.path + "/../"
    libpath   = c.path + "/../../lib/algs4.jar" + ":" + c.path + "/../../lib/stdlib.jar" 
    print(classpath)
    cmd = ["java", "-cp", classpath + ":" + libpath, "AlgoX", ifile]
    print("Executing command " + str(cmd))

    try:
        result = subprocess.check_output(cmd)
        out = []
        for i in result.splitlines():
            print ("Result = ", rescount) 
            out.append(c.generate_result(map(int, [j for j in i.split()]), ret_list))

            if ask:
                raw_input("Press enter")
            rescount += 1

    except subprocess.CalledProcessError as e:
        print ("Execution command failed:", e)

    return out


def default_input(c):
    c.reset()
    execute_n_interpret(c, None, True) 

def continuous_input(c):
    count = int(raw_input("Enter total inps"))
    for i in range(count):
        c.reset()
        print ("Enter the grid elements in NxN matrix with 0 for blanks")    
        l=[]
        for i in range(c.N):
            for e in map(int, raw_input().strip().split()):
                l.append(e)
    
        execute_n_interpret(c, l, False)
 


def register_handler():
    signal.signal(signal.SIGINT, signal_handler)


def check_valid(N):
    sN = math.sqrt(N)
    if sN * sN != N:
        print ("N is not a square number")
        exit(0)


if __name__ == '__main__':
    register_handler()

    N = int(raw_input("Enter the size of grid in N: "))
    check_valid(N)

    c = CONSTRAINT(N, sys.argv[0])

    inp = raw_input("Want to interpret results?")
    if inp == "yes":
        interpret_results(c)
    else:
        inp = raw_input("Continuous input: ")
        if inp == "yes":
            continuous_input(c)
        else:
            default_input(c)
