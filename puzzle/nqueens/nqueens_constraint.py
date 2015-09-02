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
        self.psols = []
        check = path.split("/")
        if path[0] != "/":
            path = os.getcwd() + "/" + path
        self.path = "/".join(path.split("/")[:-1])
  
    def possibilities(self):
        return self.N * self.N

    def partial_solutions(self):
        return len(self.psols)

    def trow_constraints(self):
        return self.N 

    def tcol_constraints(self):
        return self.N 
    
    #remove the corner boxes which have only 1 diagnol
    def tldiag_constraints(self):
        return 2 * self.N - 1 - 2

    #remove the corner boxes which have only 1 diagnol
    def trdiag_constraints(self):
        return 2 * self.N - 1 - 2

    def total_primary_constraints(self):
        return self.trow_constraints() + self.tcol_constraints()


    # queen in a row
    # (1,  1), (1,  2), (1,  3) ... (1, N) = 1.. N
    # total N constraints
    def row_constraint(self, d):
        (r, c) = d
        return r

    #similarly for column
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
    
     
    def total_constraints(self):
        return (self.trow_constraints()  + 
                self.tcol_constraints()  + 
                self.tldiag_constraints() +
                self.trdiag_constraints())


    def generate(self, d, result):

        trow  = self.trow_constraints()
        tcol  = self.tcol_constraints()
        trdiag  = self.trdiag_constraints()
        tldiag  = self.tldiag_constraints()

        display = False
        if len(d) > 0:
            display = True
        else:
            print  (self.possibilities(), 
                    self.total_constraints(), 
                    self.total_primary_constraints(), 
                    self.partial_solutions())


        ind = 0
        l = [i+1 for i in range(self.N)]
        for k, v in enumerate(product(l, l)):
            r, c = v
            if display:
                if ind < len(d) and d[ind] == k+1:
                    print ("Q in", (r, c))
                    result.append(c)
                    ind += 1
            else:
                if (r == self.N and c == 1) or (r == 1 and c == self.N):  # dont print rdiag
                    print(self.row_constraint(v), 
                            trow + self.col_constraint(v), 
                            trow + tcol + trdiag + self.ldiag_constraint(v))
                elif (r == 1 and c == 1) or (r == self.N and c == self.N): # dont print ldiag
                    print(self.row_constraint(v), 
                            trow + self.col_constraint(v), 
                            trow + tcol + self.rdiag_constraint(v))
                else:  
                    print(self.row_constraint(v), 
                            trow + self.col_constraint(v), 
                            trow + tcol + self.rdiag_constraint(v), 
                            trow + tcol + trdiag + self.ldiag_constraint(v))
        if not display:
            for p in self.psols:
                print(p)

    def generate_constraint(self):
        self.generate([], [])

    def check(self, result):
        return True
        for i in range(1, self.N+1):
            if result.count(i) != 1:
                return False
        
        return True

    def process(self, inp):
        for i, v in enumerate(inp):
            if v != 0:
                self.psols.append(i+1)
   
    def reset(self):
        self.psols = []


    def interpret_result(self, l):
        result = []
        l.sort()
        self.generate(l, result)
        if self.check(result):
            print("Valid Solution")
            self.draw(result)
        else:
            Print("Invalid Solution")

    def draw(self, result):
        for i in range(self.N):        
            print ("+---" * self.N, end = '')
            print("+")
            for j in range(1, self.N+1):
                if result[i] == j:
                    print("| Q ", end= '') 
                else:
                    print("|   ", end='') 
            print("|")
        print("+---" * self.N, end = '')
        print("+")
 
    def output(self, result):
        res = [0 for i in range(self.N * self.N)]
        for i in range(self.N):
            res[i*self.N + result[i] - 1] = 1
        return res

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

    ifile = "/tmp/nqueen_" + str(c.N) + ".txt" 
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
        print ("Enter the grid elements in NxN matrix with 0 for blanks and 1 for Queen")    
        l=[]
        for i in range(c.N):
            for e in map(int, raw_input().strip().split()):
                l.append(e)
    
        execute_n_interpret(c, l, False)
 


def register_handler():
    signal.signal(signal.SIGINT, signal_handler)




if __name__ == '__main__':
    register_handler()


    while True:
        inp = raw_input("Enter the size of grid in N: ")
        try:
            N = int(inp)
        except ValueError:
            print("invalid inp")
            continue

        if N > 0:
            break


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
