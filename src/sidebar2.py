import sys
from PyQt6.QtGui import QFileSystemModel, QPointingDeviceUniqueId
from PyQt6.QtWidgets import QApplication, QHBoxLayout, QStyledItemDelegate, QTreeView, QWidget,QHBoxLayout
from PyQt6.QtCore import QDir, QStandardPaths,QModelIndex, Qt
from typing import Type

class FileSystemModel(QFileSystemModel):

    def columnCount(self, parent = QModelIndex()):
        return super(FileSystemModel, self).columnCount()+1

    def data(self, index, role):
        if index.column() == self.columnCount() - 1:
            if role == Qt.ItemDataRole.DisplayRole:
                return  "YourText" #QString("YourText")

            if role == Qt.ItemDataRole.TextAlignmentRole:
                return Qt.AlignmentFlag.AlignHCenter

        return super(FileSystemModel, self).data(index, role)

# TODO: use a proxy to only show .yml files within folders

class NameDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        if isinstance(index.model(), QFileSystemModel):
            if not index.model().isDir(index):
                option.text = index.model().fileInfo(index).baseName()

    def setEditorData(self, editor, index):
        if isinstance(index.model(), QFileSystemModel):
            if not index.model().isDir(index):
                editor.setText(index.model().fileInfo(index).baseName())
            else:
                super().setEditorData(editor, index)

    def setModelData(self, editor, model, index):
        if isinstance(model, QFileSystemModel):
            fi = model.fileInfo(index)
            if not model.isDir(index):
                model.setData(index, editor.text() + "." + fi.suffix())
            else:
                super().setModelData(editor, model.index)




class Window(QWidget):

    def __init__(self):
        super().__init__()

        configLocation = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.ConfigLocation)
        userConfigLocation = configLocation+"/keyboardcontrol"
        #override
        userConfigLocation = "/home/vaisakh/vaisakhRoot/programming/python/keyboardcontrol/config/"
        print(configLocation)


        #self.model = QFileSystemModel()
        self.model = FileSystemModel()
        self.model.setRootPath(QDir.rootPath())
        self.model.setReadOnly(False)        

        self.treeview = QTreeView()
        self.treeview.setModel(self.model)
        self.treeview.setRootIndex(self.model.index(userConfigLocation))
        self.treeview.setItemDelegate(NameDelegate(self.treeview))
        for i in range(1, self.treeview.model().columnCount()):
            self.treeview.header().hideSection(i)

        layout = QHBoxLayout()

        layout.addWidget(self.treeview)
        self.setLayout(layout)



app = QApplication(sys.argv)

window = Window()
window.show()
sys.exit(app.exec())
