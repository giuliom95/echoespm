
import sys
from PySide2 import QtWidgets
from PySide2 import QtGui
from PySide2 import QtCore

import requests
import re

from pathlib import Path

IMAGES_PATH = Path('./qtapp/images/')

def getContentDataFromServer(path):
    api_url = 'http://127.0.0.1:5000'
    url = f'{api_url}/{path}/'
    # Remove multiple slashes at the end
    clean_url = re.sub('/*$', '/', url)
    r = requests.get(clean_url)
    if r.status_code / 100 != 2:
        raise RuntimeError(f'Server answered with {r.status_code}')
    return r.json()


class ExplorerElementButton(QtWidgets.QWidget):

    def __init__(self, text, pixmap):
        super().__init__()
        
        self.pixmap = pixmap
        self.text = QtWidgets.QLabel(text)
        self.icon = QtWidgets.QLabel()
        self.icon.setPixmap(self.pixmap.scaled(200,200))

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.icon)

        layout.addWidget(self.text)
        self.setLayout(layout)

        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)


class DirectoryView(QtWidgets.QScrollArea):

    def __init__(self, elements):
        super().__init__()
        self.elements = elements

        # Disable horizontal scrolling
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.grid = QtWidgets.QGridLayout()
        self.grid.setSpacing(1)

        self.elementsPerRow = 0
        self.displaceElements()

        self.setWidgetResizable(True)

        gridContainerHLayout = QtWidgets.QHBoxLayout()
        gridContainerHLayout.setContentsMargins(0,0,0,0)
        gridContainerHLayout.addLayout(self.grid)
        gridContainerHLayout.addStretch()
        gridContainerVLayout = QtWidgets.QVBoxLayout()
        gridContainerVLayout.setContentsMargins(0,0,0,0)
        gridContainerVLayout.addLayout(gridContainerHLayout)
        gridContainerVLayout.addStretch()
        gridContainer = QtWidgets.QWidget()
        gridContainer.setLayout(gridContainerVLayout)
        self.setWidget(gridContainer)
        self.grid.setContentsMargins(0,0,0,0)


    def clearGrid(self):
        itm = self.grid.takeAt(0) 
        while itm:
            self.grid.removeItem(itm)
            itm = self.grid.takeAt(0) 
            

    def displaceElements(self):
        """
        Fit elements into grid according to current size
        """
        if len(self.elements) == 0: return

        elPerRow = self.width() // self.elements[0].width()

        if elPerRow == 0:
            elPerRow = 1


        self.clearGrid()

        i = 0
        for el in self.elements:
            print(el, i // elPerRow, i % elPerRow)
            self.grid.addWidget(el, i // elPerRow, i % elPerRow)
            i += 1

        self.elementsPerRow = elPerRow

    def resizeEvent(self, event):
        self.displaceElements()



class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()

    def initUI(self):

        mainLayout = QtWidgets.QVBoxLayout()
        mainLayoutContainer = QtWidgets.QWidget()
        mainLayoutContainer.setLayout(mainLayout)

        self.addressBar = QtWidgets.QHBoxLayout()
        backToRootBtn = QtWidgets.QPushButton('content')
        backToRootBtn.setFlat(True)
        self.addressBar.addWidget(backToRootBtn)
        firstAddressSlash = QtWidgets.QLabel('/')
        self.addressBar.addWidget(firstAddressSlash)
        self.addressBar.addStretch()
        mainLayout.addLayout(self.addressBar)

        pixmap = QtGui.QPixmap(str(IMAGES_PATH.joinpath('folder.png')))

        elements = [
            ExplorerElementButton('CIAO', pixmap),
            ExplorerElementButton('CIAO', pixmap),
            ExplorerElementButton('CIAO', pixmap),
            ExplorerElementButton('CIAO', pixmap),
            ExplorerElementButton('CIAO', pixmap),
            ExplorerElementButton('CIAO', pixmap),
            ExplorerElementButton('CIAO', pixmap),
            ExplorerElementButton('CIAO', pixmap),
            ExplorerElementButton('CIAO', pixmap),
            ExplorerElementButton('CIAO', pixmap),
            ExplorerElementButton('CIAO', pixmap),
            ExplorerElementButton('CIAO', pixmap)
        ]

        directoryView = DirectoryView(elements)
        mainLayout.addWidget(directoryView)

        self.setCentralWidget(mainLayoutContainer)
        self.resize(800, 600)
        self.setWindowTitle('Test')
        self.show()
        
        


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    sys.exit(app.exec_())