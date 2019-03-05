
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


class AssetPathItem(QtWidgets.QTreeWidgetItem):
    def getFullPath(self) -> str:
        node = self
        path = []
        while node is not None:
            path.append(node.text(0))
            node = node.parent()
        return '/'.join(path[::-1])

    def removeAllChildren(self):
        c = self.child(0)
        while c is not None:
            self.removeChild(c)
            c = self.child(0)

    def requestChildren(self):
        self.removeAllChildren()
        full_path = self.getFullPath()
        data = getContentDataFromServer(full_path)
        sorted_data = sorted(data, key=lambda item: item['name'])
        for entry in sorted_data:
            item = AssetPathItem(self, [f'{entry["name"]}'])
            # No need to add children to versions
            if full_path.count('/') < 3:
                AssetPathItem(item, ['Empty'])


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()

    def initUI(self):

        # Content tree
        tree = QtWidgets.QTreeWidget()
        tree.header().hide()
        item = AssetPathItem(tree, ['content'])
        AssetPathItem(item, ['Empty'])
        tree.itemExpanded.connect(AssetPathItem.requestChildren)

        # Info panel
        l = QtWidgets.QLabel("TEST")
        b1 = QtWidgets.QPushButton("TEST1")
        b2 = QtWidgets.QPushButton("TEST2")
        leftTopLayout = QtWidgets.QVBoxLayout()
        leftTopLayout.addWidget(l)
        leftTopLayout.addStretch()
        leftTopLayout.addWidget(b1)
        leftTopLayout.addWidget(b2)
        leftTopLayoutContainer = QtWidgets.QWidget()
        leftTopLayoutContainer.setMinimumWidth(200)
        leftTopLayoutContainer.setLayout(leftTopLayout)

        mainLayout = QtWidgets.QHBoxLayout()
        mainLayout.addWidget(tree)
        mainLayout.addWidget(leftTopLayoutContainer)

        mainLayoutContainer = QtWidgets.QWidget()
        mainLayoutContainer.setLayout(mainLayout)
        self.setCentralWidget(mainLayoutContainer)

        self.resize(800, 600)
        self.setWindowTitle('Test')
        self.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    sys.exit(app.exec_())