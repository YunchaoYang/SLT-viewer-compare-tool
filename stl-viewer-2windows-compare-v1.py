# import sys

# import numpy as np
# from PyQt5.QtWidgets import QApplication
# from pyqtgraph.opengl import GLViewWidget, MeshData, GLMeshItem
# from stl import mesh

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     view = GLViewWidget()
#     # https://ozeki.hu/attachments/116/Eiffel_tower_sample.STL
#     stl_mesh = mesh.Mesh.from_file('torus.stl')

#     points = stl_mesh.points.reshape(-1, 3)
#     faces = np.arange(points.shape[0]).reshape(-1, 3)

#     mesh_data = MeshData(vertexes=points, faces=faces)
#     mesh = GLMeshItem(meshdata=mesh_data, smooth=True, drawFaces=False, drawEdges=True, edgeColor=(0, 1, 0, 1))
#     view.addItem(mesh)

#     view.show()
#     app.exec()

# import sys
# import pyqtgraph.opengl as gl
# from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout

# class MyMainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.active_glvw = None  # To track the active GLViewWidget

#         self.initUI()

#     def initUI(self):
#         self.setWindowTitle('Multiple GLViewWidgets')
#         self.setGeometry(100, 100, 800, 600)

#         central_widget = QWidget(self)
#         self.setCentralWidget(central_widget)

#         layout = QGridLayout(central_widget)

#         glvw1 = gl.GLViewWidget()
#         glvw2 = gl.GLViewWidget()

#         layout.addWidget(glvw1, 0, 0)
#         layout.addWidget(glvw2, 0, 1)

#         # Add content to the GLViewWidgets (for demonstration)
#         self.addContentToGLViewWidget(glvw1, 'GLViewWidget 1')
#         self.addContentToGLViewWidget(glvw2, 'GLViewWidget 2')

#         # Connect drag and drop events
#         glvw1.setAcceptDrops(True)
#         glvw1.installEventFilter(self)
#         glvw2.setAcceptDrops(True)
#         glvw2.installEventFilter(self)

#     def eventFilter(self, source, event):
#         if event.type() == event.DragEnter:
#             # Set the active GLViewWidget based on the source widget
#             if source is self.active_glvw:
#                 return super().eventFilter(source, event)  # Allow the drag event to continue
#             self.active_glvw = source
#             return True
#         elif event.type() == event.Drop:
#             if self.active_glvw is not None:
#                 # Handle the drop event for the active GLViewWidget
#                 dropped_text = event.mimeData().text()
#                 print(f"Data dropped in {self.active_glvw.windowTitle()}: {dropped_text}")
#                 # Handle the drop event for the active GLViewWidget here
#                 return True
#         return super().eventFilter(source, event)

#     def addContentToGLViewWidget(self, glvw, title):
#         # Add content to the GLViewWidget (for demonstration)
#         glvw.addItem(gl.GLAxisItem())
#         glvw.addItem(gl.GLSurfacePlotItem(shading='smooth'))
#         glvw.setWindowTitle(title)

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = MyMainWindow()
#     window.show()
#     sys.exit(app.exec_())


# import sys
# import pyqtgraph.opengl as gl
# from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QPushButton

# class GLViewWidgetWrapper(QWidget):
#     def __init__(self, title):
#         super().__init__()
#         self.initUI(title)

#     def initUI(self, title):
#         layout = QGridLayout(self)
        
#         self.glvw = gl.GLViewWidget()
#         layout.addWidget(self.glvw, 0, 0)
        
#         self.addContentToGLViewWidget(title)

#         # Create and add a button to the layout
#         self.button = QPushButton('Click Me', self)
#         layout.addWidget(self.button, 1, 0)

#     def addContentToGLViewWidget(self, title):
#         # Add content to the GLViewWidget (for demonstration)
#         self.glvw.addItem(gl.GLAxisItem())
#         self.glvw.addItem(gl.GLSurfacePlotItem(shading='smooth'))
#         self.glvw.setWindowTitle(title)

# class MyMainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()

#         self.initUI()

#     def initUI(self):
#         self.setWindowTitle('Multiple GLViewWidgets with Buttons')
#         self.setGeometry(100, 100, 800, 600)

#         central_widget = QWidget(self)
#         self.setCentralWidget(central_widget)

#         layout = QGridLayout(central_widget)

#         glvw1 = GLViewWidgetWrapper('GLViewWidget 1')
#         glvw2 = GLViewWidgetWrapper('GLViewWidget 2')

#         layout.addWidget(glvw1, 0, 0)
#         layout.addWidget(glvw2, 0, 1)

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = MyMainWindow()
#     window.show()
#     sys.exit(app.exec_())


import sys
import pyqtgraph.opengl as gl
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QPushButton, QFileDialog

import stl
import numpy as np

from pathlib import Path

class GLViewWidgetWrapper(QWidget):
    def __init__(self, title):
        super().__init__()
        self.initUI(title)

        self.currentSTL = None
        self.lastDir = None
        
        self.droppedFilename = None

    def initUI(self, title):
        layout = QGridLayout(self)
        
        self.glvw = gl.GLViewWidget()
        layout.addWidget(self.glvw, 0, 0)
        
        #self.addContentToGLViewWidget(title)

        g = gl.GLGridItem()
        g.setSize(200, 200)
        g.setSpacing(5, 5)
        self.glvw.addItem(g)

        # Create and add a button to the layout
        self.button = QPushButton('Load STL', self)
        layout.addWidget(self.button, 1, 0)
        self.button.clicked.connect(self.showDialog)

        # Enable drag and drop for the GLViewWidgetWrapper
        self.setAcceptDrops(True)

    def addContentToGLViewWidget(self, title):
        # Add content to the GLViewWidget (for demonstration)
        self.glvw.addItem(gl.GLAxisItem())
        self.glvw.addItem(gl.GLSurfacePlotItem(shading='smooth'))
        self.glvw.setWindowTitle(title)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            print(f'Dropped file: {file_path}')

            if file_path.lower().endswith('.stl'):
                # Handle the STL file drop (for example, load and display it)
                print(f"rendering {file_path}")
                self.showSTL(file_path)
                self.lastDir = Path(file_path[0]).parent
                
    def showDialog(self):
        directory = Path("")
        if self.lastDir:
            directory = self.lastDir
        fname = QFileDialog.getOpenFileName(self, "Open file", str(directory), "STL (*.stl)")
        print(fname[0])
        if fname[0]:
            self.showSTL(fname[0])
            self.lastDir = Path(fname[0]).parent

    # def loadSTL(self, stl_file):
    #     # Load and display the STL file using pyqtgraph's GLViewWidget
    #     self.glvw.clear()  # Clear existing content
    #     self.glvw.addItem(gl.GLSTLRenderer(file_path=stl_file))
    #     self.glvw.setWindowTitle(f'{self.windowTitle()} - STL Viewer')
         
    def showSTL(self, filename):
        self.glvw.clear()
        # if self.currentSTL:
        #     self.glvw.removeItem(self.currentSTL)

        points, faces = self.loadSTL(filename)
        #print(points, faces)
        meshdata = gl.MeshData(vertexes=points, faces=faces)
        mesh = gl.GLMeshItem(meshdata=meshdata, smooth=True, drawFaces=True, drawEdges=True, shader="shaded", edgeColor=(0, 1, 0, 1))
        self.glvw.addItem(mesh)
        
        self.currentSTL = mesh
        
    def loadSTL(self, filename):
        m = stl.mesh.Mesh.from_file(filename)
        shape = m.points.shape
        points = m.points.reshape(-1, 3)
        faces = np.arange(points.shape[0]).reshape(-1, 3)
        return points, faces
    
class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Multiple GLViewWidgets with Drag and Drop')
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QGridLayout(central_widget)

        glvw1 = GLViewWidgetWrapper('GLViewWidget 1')
        glvw2 = GLViewWidgetWrapper('GLViewWidget 2')

        layout.addWidget(glvw1, 0, 0)
        layout.addWidget(glvw2, 0, 1)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec_())
