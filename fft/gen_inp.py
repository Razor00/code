#!/usr/bin/python

import sys
import random as r
if len(sys.argv) == 1:
    n = int(raw_input("Enter the number of digits to generate: "))
else:
    n = int(sys.argv[1])

m = n / 10
s = n % 10
a = [i for i in range(10)]
for i in range(m):
    r.shuffle(a)
    for v in a:
        print v,

a = [i for i in range(s)]
r.shuffle(a)
for v in a:
    print v,
print
