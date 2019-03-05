
import sys
from PySide2 import QtWidgets
from PySide2 import QtGui
from PySide2 import QtCore

import requests

api_url = 'http://127.0.0.1:5000'

class AssetPathItem(QtWidgets.QTreeWidgetItem):
    def getFullPath(self) -> str:
        node = self
        path = []
        while node is not None:
            path.append(node.text(0))
            node = node.parent()
        return '/'.join(path[::-1])

    def removeAllChildren(self):
        for ci in range(self.childCount()):
            c = self.child(ci)
            self.removeChild(c)

    def requestChildren(self):
        self.removeAllChildren()
        url = f'{api_url}/content/{self.getFullPath()}/'
        r = requests.get(url)
        if r.status_code / 100 != 2: sys.exit()
        data = r.json()
        for entry in data:
            item = AssetPathItem(self, [f'{entry["name"]}'])
            AssetPathItem(item, ['Empty'])


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()

    def initUI(self):
        tree = QtWidgets.QTreeWidget()
        tree.header().hide()

        r = requests.get(f'{api_url}/content/')
        if r.status_code / 100 != 2: sys.exit()
        data = r.json()

        for entry in data:
            item = AssetPathItem(tree, [f'{entry["name"]}'])
            AssetPathItem(item, ['Empty'])
            
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