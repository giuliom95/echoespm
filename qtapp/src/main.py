
import sys
from PySide2 import QtWidgets
from PySide2 import QtGui
from PySide2 import QtCore

import requests

class AssetPathItem(QtWidgets.QTreeWidgetItem):
    def getFullPath(self) -> str:
        node = self
        path = []
        while node is not None:
            path.append(node.text(0))
            node = node.parent()
        return '/' + '/'.join(path[::-1]) + '/'

    def requestChildren(self):
        print("Hello World: {0}".format(self.getFullPath()))


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()

    def initUI(self):
        tree = QtWidgets.QTreeWidget()
        tree.header().hide()
        for i in range(10):
            item = AssetPathItem(tree, ['{0}'.format(i)])
            for j in range(20):
                subitem = AssetPathItem(item, ['{0}'.format(j)])
        tree.itemExpanded.connect(AssetPathItem.requestChildren)

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