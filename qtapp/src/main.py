
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
    class Levels():
        root = 0
        content_type = 1
        content = 2
        resource = 3
        version = 4

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

    def getLevel(self):
        level = -1
        node = self
        while node is not None:
            level += 1
            node = node.parent()
        return level

    def requestChildren(self):
        self.removeAllChildren()
        full_path = self.getFullPath()
        data = getContentDataFromServer(full_path)
        sorted_data = sorted(data, key=lambda item: item['name'])
        for entry in sorted_data:
            item = AssetPathItem(self, [f'{entry["name"]}'])
            # No need to add children to versions
            if self.getLevel() != AssetPathItem.Levels.resource:
                # Add dummy node to make children expandable
                AssetPathItem(item, ['Empty'])  


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()

    def initUI(self):

        # Content tree
        self.tree = QtWidgets.QTreeWidget()
        self.tree.header().hide()
        item = AssetPathItem(self.tree, ['content'])
        AssetPathItem(item, ['Empty'])
        self.tree.itemExpanded.connect(AssetPathItem.requestChildren)
        self.tree.itemSelectionChanged.connect(self.treeSelectionChanged)

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
        mainLayout.addWidget(self.tree)
        mainLayout.addWidget(leftTopLayoutContainer)

        mainLayoutContainer = QtWidgets.QWidget()
        mainLayoutContainer.setLayout(mainLayout)
        self.setCentralWidget(mainLayoutContainer)

        self.resize(800, 600)
        self.setWindowTitle('Test')
        self.show()

    def treeSelectionChanged(self):
        current_level = 0

        selection = self.tree.selectedItems()
        if len(selection) == 1:
            current_level = selection[0].getLevel()

        print(current_level)
        


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    sys.exit(app.exec_())