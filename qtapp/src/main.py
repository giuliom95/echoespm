
import sys
from PySide2 import QtWidgets
from PySide2 import QtGui
from PySide2 import QtCore

import requests

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()

    def initUI(self):
        
        tree = QtWidgets.QTreeWidget()
        tree.header().hide()
        items = [QtWidgets.QTreeWidgetItem(tree, ['{0}'.format(i)]) for i in range(10)]
        subitems = [
            [
                QtWidgets.QTreeWidgetItem(item, ['{0}'.format(j)]) 
                for j in range(20)
            ] 
            for item in items
        ]

        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addWidget(tree)

        centralWidget = QtWidgets.QWidget()
        centralWidget.setLayout(mainLayout)
        self.setCentralWidget(centralWidget)

        self.resize(800, 600)
        self.setWindowTitle('Test')
        self.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    sys.exit(app.exec_())