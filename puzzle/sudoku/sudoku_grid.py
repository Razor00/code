#!/usr/bin/python
import sys
import math
from PyQt4 import QtGui
from PyQt4.QtGui import QWidget, QApplication

from sudoku_constraint import CONSTRAINT, execute_n_interpret

class SUDOKU_GRID(QtGui.QGraphicsView):
    @staticmethod
    def maxDigits(n):
        p = 0
        while n:
            n = n/10
            p += 1
        return p

    def cleardata(self):
        for i in range(self.N):
            for j in range(self.N):
                edt = self.layout.itemAt(i, j).graphicsItem().widget()
                edt.setText("")
        self.inp = None
        self.result = None
         

    def fetchdata(self, lbl):
        inp = []
        lbl.setText("")
        for i in range(self.N):
            for j in range(self.N):
                edt = self.layout.itemAt(i, j).graphicsItem().widget()
                txt = edt.text()
                if txt == "":
                    v = 0
                else:
                    try:
                        v = int(txt)
                    except ValueError:
                        lbl.setStyleSheet("color: rgb(255, 0, 0);")
                        outmsg = "Invalid Value at " + "(" + str(i+1) + "," + str(j+1) + "): " + txt
                        lbl.setText(outmsg)
                        return None

                if not (v >= 0 and v <=  N):
                    lbl.setStyleSheet("color: rgb(255, 0, 0);")
                    outmsg = "Invalid Value at " + "(" + str(i+1) + "," \
                            + str(j+1) + ") " + txt + ": Only 0 to " + str(N) + " are allowed"         
                    lbl.setText(outmsg)
                    return None
                        
                inp.append(v) 

               
        return inp

    def filldata(self, result, idx, lbl):
        res = result[idx]
        font = QtGui.QFont()
        font.setBold(True)
        font.setPointSize(12)
        lbl.setFont(font)
        lbl.setStyleSheet("color : black")
        lbl.setText("Solutions " + "(" + str(len(result)) + ")" + ":" + str(idx+1))
        print(res)
        k = 0
        for i in range(self.N):
            for j in range(self.N):
                edt = self.layout.itemAt(i, j).graphicsItem().widget()
                if self.inp[k] == 0:
                    edt.setStyleSheet("color: rgb(0, 102, 0);")
                else:
                    edt.setStyleSheet("color: rgb(0, 0, 255);")
                edt.setText(str(res[k]))
                k += 1

    def next(self, lbl):
        if self.inp and self.result:
            size = len(self.result)
            if size > 0:
                if self.res_idx != size:
                    self.filldata(self.result, self.res_idx, lbl)
                    self.res_idx += 1
                else:
                    lbl.setText("Reached last solution")
        else:
            lbl.setStyleSheet("color: rgb(255, 0, 0);")
            lbl.setText("CANNOT BE SOLVED!!!")


    def solve(self, lbl):
        self.inp = self.fetchdata(lbl)
        if self.inp == None:
            return

        c = CONSTRAINT(self.N, self.path)
        self.result = execute_n_interpret(c, self.inp, False, True)
        self.res_idx = 0
        self.next(lbl)

    def __init__(self, N, path):
        super(SUDOKU_GRID, self).__init__()
        self.path = path
        self.inp  = None
        self.result = None
        self.N = N;
        self.bw = 40
        self.bh = 40
        self.hs = 8
        self.vs = 8
        scene = QtGui.QGraphicsScene(self)
        scene.setItemIndexMethod(QtGui.QGraphicsScene.NoIndex)
        scene.setSceneRect(0, 0, (self.bw + self.hs) * N, (self.bh + self.vs) * N)
        self.setScene(scene)
        self.setCacheMode(QtGui.QGraphicsView.CacheBackground)
        self.setViewportUpdateMode(QtGui.QGraphicsView.BoundingRectViewportUpdate)
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setTransformationAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtGui.QGraphicsView.AnchorViewCenter)

        self.max = SUDOKU_GRID.maxDigits(self.N)
        self.layout = QtGui.QGraphicsGridLayout()
        self.layout.setHorizontalSpacing(self.hs)
        self.layout.setVerticalSpacing(self.vs)
        bpen = QtGui.QPen()
        pen = QtGui.QPen()
        #pen.setColor(QtGui.QColor("red"))
        pen.setWidth(3)
        sN = int(math.sqrt(N))
        for i in range(N):
            x1 = 0
            y1 = i * (self.bh + self.vs)
            x2 = N * (self.bw + self.hs)
            y2 = y1
            if i % sN == 0:
                scene.addLine(x1, y1, x2, y2, pen) 
            else:
                scene.addLine(x1, y1, x2, y2) 

            font = QtGui.QFont("Times", 14, QtGui.QFont.Bold, True)
            for j in range(N):
                ledt = QtGui.QLineEdit()
                ledt.setMaxLength(self.max)
                ledt.setMaximumSize(self.bw, self.bh)
                ledt.setMinimumSize(self.bw, self.bh)
                ledt.setFont(font)
                proxy = scene.addWidget(ledt)
                self.layout.addItem(proxy,  i, j)
                
                x_1 = (j) * (self.bw + self.hs)
                y_1 = 0
                x_2 = x_1
                y_2 = N * (self.bh + self.vs)
                if j % sN == 0:
                    scene.addLine(x_1, y_1, x_2, y_2, pen)
                else:
                    scene.addLine(x_1, y_1, x_2, y_2)


                
            x_1 = (j+1) * (self.bw + self.hs)
            y_1 = 0
            x_2 = x_1
            y_2 = N * (self.bh + self.vs)
            if (j+1) % sN == 0:
                scene.addLine(x_1, y_1, x_2, y_2, pen)
            else: 
                scene.addLine(x_1, y_1, x_2, y_2)


        x1 = 0
        x1 = 0
        y1 = (i+1) * (self.bh + self.vs)
        x2 = N * (self.bw + self.hs)
        y2 = y1
        if (i+1) % sN == 0:
            scene.addLine(x1, y1, x2, y2, pen) 
        else:
            scene.addLine(x1, y1, x2, y2) 

        print self.layout.horizontalSpacing(), self.layout.verticalSpacing()

        gw = QtGui.QGraphicsWidget()
        gw.setLayout(self.layout);
        scene.addItem(gw)
        self.move(400, 400)
        self.ensureVisible(0, 0, 800, 800)


while True:
    s = raw_input("Please enter the grid dimension: ")
    if not s:
        continue

    inp = s.strip().split()
    if len(inp) == 0:
        continue
    
    try:
        N = int(inp[0])
    except  ValueError:
        print("Please enter a positive Integer square")
        continue

    if N <= 0:
        print ("Sudoku needs a positive Integer Square number")
        continue

    p = int(math.sqrt(N))
    if p * p == N:
        break
    else:
        print (str(N) + " is not a square")

a = QApplication(sys.argv)
grid = SUDOKU_GRID(N, sys.argv[0])
main_layout   = QtGui.QVBoxLayout()
top_layout    = QtGui.QHBoxLayout()
middle_layout = QtGui.QHBoxLayout()
bottom_layout = QtGui.QGridLayout()

status_lbl  = QtGui.QLabel()
status_lbl.setAutoFillBackground(True)

solve_btn = QtGui.QPushButton(text = "Solve")
solve_btn.clicked.connect(lambda: grid.solve(status_lbl))

next_btn  = QtGui.QPushButton(text = "Next")
next_btn.clicked.connect(lambda: grid.next(status_lbl))

clear_btn = QtGui.QPushButton(text = "Clear")
clear_btn.clicked.connect(grid.cleardata)

exit_btn = QtGui.QPushButton(text = "Exit")
exit_btn.clicked.connect(sys.exit)



top_layout.addWidget(grid)
middle_layout.addWidget(status_lbl)
bottom_layout.addWidget(solve_btn, 0, 0)
bottom_layout.addWidget(next_btn, 0, 1)
bottom_layout.addWidget(clear_btn, 1, 0)
bottom_layout.addWidget(exit_btn, 1, 1)


main_layout.addLayout(top_layout)
main_layout.addLayout(middle_layout)
main_layout.addLayout(bottom_layout)

w = QWidget()
w.setWindowTitle("Sudoku " + str(N) + "x" + str(N))
w.setLayout(main_layout)
w.show()
sys.exit(a.exec_())
