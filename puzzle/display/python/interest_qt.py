#!/usr/bin/python
from PyQt4.QtGui import  *
from PyQt4.QtCore import *

import sys
def clear(edt):
    if edt:
        edt.setText("")
    else:
        for k in inp:
            inp[k][2].setText("0")


def get_value(identity):
    edt = inp[identity][2]
    try:
        v = float(edt.text())
    except ValueError:
        clear(edt)
        v = 0
    
    return v


def fetch_values():
    P = float(get_value("P"))
    R = float(get_value("R"))
    S = float(get_value("S"))
    T = float(get_value("T"))
    return P, R, S, T

def set_interest(v):
        inp["I"][2].setText(str(v))

def calculate_compound():
    (P, R, S, T) = fetch_values()
    if S == 0:
        set_interest("Step cannot be zero")
    else:
        v = (P * (1 + R/(S*100.0))**(S*T)) - P
        set_interest(v)

def calculate_simple():
    (P, R, S, T) = fetch_values()
    set_interest((P*T*R/100.0))

def exit():
    import sys
    sys.exit(0)

inp = {"P" : [0, "Principal"], "R" : [1, "Rate of Interest"], "S" : [2, "Step Per Year"], "T": [3, "Number of years"],  "I" : [4, "Interest"]}
out = {"C" : [0, "Compound Interest", calculate_compound],  "S" : [1, "Simple Interest", calculate_simple], "R" : [2, "Clear", clear], "E" : [3, "Exit", exit] }

app = QApplication(sys.argv) #ignore()
window = QWidget()
window.setWindowTitle("Calculator")
window.show()

layout = QGridLayout(window) 

# [Add widgets to the widget]
# Create some widgets (these won't appear immediately):
for k in inp:
    lbl = QLabel(inp[k][1])
    edt = QLineEdit()
    inp[k].append(edt)
    layout.addWidget(lbl, inp[k][0], 0) 
    layout.addWidget(edt, inp[k][0], 1, 1, 2) 
    layout.setRowStretch(inp[k][0], 2)

btngroup = QButtonGroup()
off = len(inp)
for k in out:
    btn = QPushButton(out[k][1], window)
    out[k].append(btn)
    btngroup.addButton(btn, out[k][0])
    layout.addWidget(btn, off, out[k][0]) #, out[k][0], 0)
    btn.clicked.connect(out[k][2])

# Let's resize the window:
window.resize(480, 160)

clear(None)

# Start the event loop...
sys.exit(app.exec_())
