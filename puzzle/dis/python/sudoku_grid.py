#!/usr/bin/python
import sys
import math
from PyQt4 import QtGui
from PyQt4.QtGui import QWidget, QApplication


class SUDOKU_GRID(QtGui.QGraphicsView):
    @staticmethod
    def maxDigits(n):
        p = 0
        while n:
            n = n/10
            p += 1
        return p

    def __init__(self, N):
        super(SUDOKU_GRID, self).__init__()
        self.N = N;
        self.bw = 40
        self.bh = 40
        scene = QtGui.QGraphicsScene(self)
        scene.setItemIndexMethod(QtGui.QGraphicsScene.NoIndex)
        scene.setSceneRect(0, 0, (self.bw + 3) * N, self.bh * N)
        self.setScene(scene)
        self.setCacheMode(QtGui.QGraphicsView.CacheBackground)
        self.setViewportUpdateMode(QtGui.QGraphicsView.BoundingRectViewportUpdate)
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setTransformationAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtGui.QGraphicsView.AnchorViewCenter)

        self.max = SUDOKU_GRID.maxDigits(self.N)
        layout = QtGui.QGraphicsGridLayout()
        for i in range(N):
            for j in range(N):
                ledt = QtGui.QLineEdit()
                ledt.setMaxLength(self.max)
                ledt.setMaximumSize(self.bw, self.bh)
                ledt.setMinimumSize(self.bw, self.bh)
                proxy = scene.addWidget(ledt)
                layout.addItem(proxy,  i, j)
                print proxy.sceneBoudingRect()
 
                
   
        print layout.horizontalSpacing(), layout.verticalSpacing()

        gw = QtGui.QGraphicsWidget()
        gw.setLayout(layout);
        scene.addItem(gw)

        self.move(400, 400)
        self.ensureVisible(400, 400, 400, 400)
        #self.resize(1000, 1000)
        #self.show()


N = int(raw_input("Please enter the grid dimension: "))
p = math.sqrt(N)
if p * p != N:
    print ("N is not a square")
    sys.exit(0)

a = QApplication(sys.argv)
grid = SUDOKU_GRID(N)
main_layout   = QtGui.QVBoxLayout()
top_layout    = QtGui.QHBoxLayout()
bottom_layout = QtGui.QHBoxLayout()

psh_btn1 = QtGui.QPushButton(text = "solve")
psh_btn2 = QtGui.QPushButton(text = "exit")

psh_btn2.clicked.connect(sys.exit)
bottom_layout.addWidget(psh_btn1)
bottom_layout.addWidget(psh_btn2)
top_layout.addWidget(grid)
main_layout.addLayout(top_layout)
main_layout.addLayout(bottom_layout)

w = QWidget()
w.setWindowTitle("Sudoku " + str(N) + "x" + str(N))
w.setLayout(main_layout)
w.show()
sys.exit(a.exec_())
