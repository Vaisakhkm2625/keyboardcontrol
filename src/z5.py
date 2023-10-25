import sys
import os
from PyQt6.QtCore import QDir
from PyQt6.QtWidgets import QApplication, QMainWindow, QTreeView, QVBoxLayout, QPushButton, QWidget, QFileDialog, QInputDialog, QLineEdit
from PyQt6.QtGui import QFileSystemModel

class FileTreeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle("File Tree Viewer")

        self.model = QFileSystemModel()
        self.model.setRootPath(os.path.expanduser('~'))
        #self.model.setFilter(QDir.Files | QDir.AllDirs)
        self.model.setNameFilters(['*.yml'])
        self.model.setNameFilterDisables(False)

        self.treeView = QTreeView(self)
        self.treeView.setModel(self.model)
        self.treeView.setColumnWidth(0, 250)
        self.treeView.setRootIndex(self.model.index(os.path.expanduser('~')))

        self.createButton = QPushButton("Create")
        self.createButton.clicked.connect(self.createItem)
        self.deleteButton = QPushButton("Delete")
        self.deleteButton.clicked.connect(self.deleteItem)
        self.renameButton = QPushButton("Rename")
        self.renameButton.clicked.connect(self.renameItem)

        self.layout1 = QVBoxLayout()
        self.layout1.addWidget(self.treeView)
        self.layout1.addWidget(self.createButton)
        self.layout1.addWidget(self.deleteButton)
        self.layout1.addWidget(self.renameButton)

        self.container = QWidget()
        self.container.setLayout(self.layout1)

        self.setCentralWidget(self.container)

    def createItem(self):
        path = self.model.filePath(self.treeView.currentIndex())
        if not path:
            path = os.path.expanduser('~')
        name, ok = QInputDialog.getText(self, "Create Item", "Enter the name:")
        if ok:
            path = os.path.join(path, name)
            if self.treeView.model().isDir(self.treeView.currentIndex()):
                os.mkdir(path)
            else:
                with open(path, 'w') as f:
                    pass
            #self.model.refresh()

    def deleteItem(self):
        index = self.treeView.currentIndex()
        if index.isValid():
            path = self.model.filePath(index)
            if os.path.exists(path):
                if self.treeView.model().isDir(index):
                    os.rmdir(path)
                else:
                    os.remove(path)
                #self.model.refresh()

    def renameItem(self):
        index = self.treeView.currentIndex()
        if index.isValid():
            path = self.model.filePath(index)
            #new_name, ok = QInputDialog.getText(self, "Rename Item", "Enter the new name:", QLineEdit.Normal, os.path.basename(path))

            new_name, ok =QInputDialog.getText(self, "Create Item", "Enter the name:")
            if ok:
                new_path = os.path.join(os.path.dirname(path), new_name)
                os.rename(path, new_path)
                #self.model.refresh()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FileTreeApp()
    ex.show()
    sys.exit(app.exec())
