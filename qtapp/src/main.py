
import sys
from PySide2 import QtWidgets
from PySide2 import QtGui
from PySide2 import QtCore

import requests
import re

import random

def getContentDataFromServer(path):
    api_url = 'http://127.0.0.1:5000'
    url = f'{api_url}/{path}/'
    # Remove multiple slashes at the end
    clean_url = re.sub('/*$', '/', url)
    r = requests.get(clean_url)
    if r.status_code / 100 != 2:
        raise RuntimeError(f'Server answered with {r.status_code}')
    return r.json()


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
        self.addressBar.addWidget(backToRootBtn)
        firstAddressSlash = QtWidgets.QLabel('/')
        self.addressBar.addWidget(firstAddressSlash)
        self.addressBar.addStretch()
        mainLayout.addLayout(self.addressBar)

        dirGrid = QtWidgets.QGridLayout()
        dirGrid.addWidget(QtWidgets.QPushButton('CIAO'),0,0)
        dirGrid.addWidget(QtWidgets.QPushButton('CIAO'),0,1)
        dirGrid.addWidget(QtWidgets.QPushButton('CIAO'),0,2)
        dirGrid.addWidget(QtWidgets.QPushButton('CIAO'),1,0)
        dirGrid.addWidget(QtWidgets.QPushButton('CIAO'),1,1)
        dirGrid.addWidget(QtWidgets.QPushButton('CIAO'),1,2)

        dirGridContainer = QtWidgets.QWidget()
        dirGridContainer.setLayout(dirGrid)

        currentDirScrollableArea = QtWidgets.QScrollArea()
        currentDirScrollableArea.setWidget(dirGridContainer)
        mainLayout.addWidget(currentDirScrollableArea)

        self.setCentralWidget(mainLayoutContainer)
        self.resize(800, 600)
        self.setWindowTitle('Test')
        self.show()
        
        


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    sys.exit(app.exec_())