from PyQt5 import QtWidgets  

from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
import pyqtgraph.opengl as gl

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *  

import numpy as np
from stl import mesh

from pathlib import Path
        
class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setGeometry(0, 0, 700, 900) 
        self.setAcceptDrops(True)
        
        self.initUI()
        
        self.currentSTL = None
        self.currentSTL1 = None
        self.currentSTL2 = None
        self.lastDir = None
        
        self.droppedFilename = None
    
    def initUI(self):
        centerWidget = QWidget()
        self.setCentralWidget(centerWidget)
        
        layout = QVBoxLayout()
        centerWidget.setLayout(layout)
        
        
        # top viewer
        self.viewer = gl.GLViewWidget()
        layout.addWidget(self.viewer, 1)
        
        self.viewer.setWindowTitle('STL Viewer')
        self.viewer.setCameraPosition(distance=40)
        self.viewer.setObjectName("viewer1")
        g = gl.GLGridItem()
        g.setSize(200, 200)
        g.setSpacing(5, 5)
        self.viewer.addItem(g)

        btn = QPushButton(text="Load STL")
        btn.setObjectName("btn1")
        btn.clicked.connect(self.showDialog)
        btn.setFont(QFont("Ricty Diminished", 14))
        layout.addWidget(btn)


        # bottom viewer
        self.viewer2 = gl.GLViewWidget()
        layout.addWidget(self.viewer2, 1)

        self.viewer2.setWindowTitle('STL Viewer2')
        self.viewer2.setCameraPosition(distance=40)
        self.viewer.setObjectName("viewer2")

        g2 = gl.GLGridItem()
        g2.setSize(200, 200)
        g2.setSpacing(5, 5)
        self.viewer2.addItem(g2)

        btn2 = QPushButton(text="Load STL2")
        btn2.setObjectName("btn2")
        btn2.clicked.connect(self.showDialog)
        btn2.setFont(QFont("Ricty Diminished", 14))
        layout.addWidget(btn2)


    def showDialog(self):
        sender = self.sender() # use the sender() method of the QObject class to identify the sender of the signal
        directory = Path("")
        if self.lastDir:
            directory = self.lastDir
        fname = QFileDialog.getOpenFileName(self, "Open file", str(directory), "STL (*.stl)")
        if fname[0]:
            if sender is not None and isinstance(sender, QPushButton):
                button_text = sender.text()                
                self.showSTL(fname[0], button_text)
                self.lastDir = Path(fname[0]).parent
            
    def showSTL(self, filename, button_text):
        if button_text == "Load STL" and self.currentSTL1:
            self.viewer.removeItem(self.currentSTL1)
        if button_text == "Load STL2" and self.currentSTL2:
            self.viewer.removeItem(self.currentSTL2)

        points, faces = self.loadSTL(filename)
        meshdata = gl.MeshData(vertexes=points, faces=faces)
        mesh = gl.GLMeshItem(meshdata=meshdata, smooth=True, drawFaces=False, drawEdges=True, edgeColor=(0, 1, 0, 1))
        
        if button_text == "Load STL":
            self.viewer.addItem(mesh)
            self.currentSTL1 = mesh
        if button_text == "Load STL2":
            self.viewer2.addItem(mesh)
            self.currentSTL2 = mesh

        
    def loadSTL(self, filename):
        m = mesh.Mesh.from_file(filename)
        shape = m.points.shape
        points = m.points.reshape(-1, 3)
        faces = np.arange(points.shape[0]).reshape(-1, 3)
        return points, faces

    # def dragEnterEvent(self, e):
    #     print("enter")
    #     mimeData = e.mimeData()
    #     mimeList = mimeData.formats()
    #     filename = None
        
    #     if "text/uri-list" in mimeList:
    #         filename = mimeData.data("text/uri-list")
    #         filename = str(filename, encoding="utf-8")
    #         filename = filename.replace("file:///", "").replace("\r\n", "").replace("%20", " ")
    #         filename = Path(filename)
            
    #     if filename.exists() and filename.suffix == ".stl":
    #         e.accept()
    #         self.droppedFilename = filename
    #     else:
    #         e.ignore()
    #         self.droppedFilename = None
        
    # def dropEvent(self, e):
    #     if self.droppedFilename:
    #         self.showSTL(self.droppedFilename)

if __name__ == '__main__':
    
    #app = QtGui.QApplication([])
    app = QtWidgets.QApplication([])

    window = MyWindow()
    window.show()
    app.exec_()