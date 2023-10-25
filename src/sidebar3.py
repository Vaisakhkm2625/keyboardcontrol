import os
import sys
from PyQt6.QtGui import QAction, QFileSystemModel, QPointingDeviceUniqueId
from PyQt6.QtWidgets import QApplication, QHBoxLayout, QInputDialog, QLabel, QMenu, QPushButton, QStyledItemDelegate, QTreeView, QWidget,QHBoxLayout
from PyQt6.QtCore import QDir, QStandardPaths,QModelIndex, Qt, pyqtSignal

# class FileSystemModel(QFileSystemModel):
#
#     def columnCount(self, parent = QModelIndex()):
#         return super(FileSystemModel, self).columnCount()+1
#
#     def data(self, index, role):
#         if index.column() == self.columnCount() - 1:
#             if role == Qt.ItemDataRole.DisplayRole:
#                 return  "YourText" #QString("YourText")
#
#             if role == Qt.ItemDataRole.TextAlignmentRole:
#                 return Qt.AlignmentFlag.AlignHCenter
#
#         return super(FileSystemModel, self).data(index, role)

# TODO: use a proxy to only show .yml files within folders

    #class NameDelegate(QStyledItemDelegate):
    #
    #    def initStyleOption(self, option, index):
    #        super().initStyleOption(option, index)
    #        if isinstance(index.model(), QFileSystemModel):
    #            if not index.model().isDir(index):
    #                option.text = index.model().fileInfo(index).baseName()
    #
    #    def setEditorData(self, editor, index):
    #        if isinstance(index.model(), QFileSystemModel):
    #            if not index.model().isDir(index):
    #                editor.setText(index.model().fileInfo(index).baseName())
    #            else:
    #                super().setEditorData(editor, index)
    #
    #    def setModelData(self, editor, model, index):
    #        if isinstance(model, QFileSystemModel):
    #            fi = model.fileInfo(index)
    #            if not model.isDir(index):
    #                model.setData(index, editor.text() + "." + fi.suffix())
    #            else:
    #                super().setModelData(editor, model.index)
    #


class CustomFileSystemModel(QFileSystemModel):
    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole and index.isValid() and index.column() == 0:
            # Get the file name without extension
            fileName = super().data(index, Qt.ItemDataRole.DisplayRole)
            extensionIndex = fileName.rfind('.')
            if extensionIndex != -1:
                fileName = fileName[:extensionIndex]
            return fileName
        return super().data(index, role)


class ConfigTreeView(QWidget):

    fileClicked = pyqtSignal(str)

    def __init__(self,userConfigLocation):
        super().__init__()

        self.treeview = QTreeView()

        self.userConfigLocation = userConfigLocation
        self.setupModel()
        self.setup_ui()

        #self.treeview.setItemDelegate(NameDelegate(self))

        self.treeview.clicked.connect(self._configClicked)

        layout = QHBoxLayout()
        layout.addWidget(self.treeview)
        self.setLayout(layout)

    def setupModel(self):
        self.model = CustomFileSystemModel()
        self.model.setRootPath(QDir.rootPath())
        self.model.setNameFilters(["*.yml"])
        self.model.setNameFilterDisables(False)

    def setup_ui(self):
        self.treeview.setModel(self.model)
        self.treeview.setRootIndex(self.model.index(self.userConfigLocation))

        self.treeview.hideColumn(1)  # Hide size column
        self.treeview.hideColumn(2)  # Hide type column
        self.treeview.hideColumn(3)  # Hide date modified column

        self.treeview.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.treeview.customContextMenuRequested.connect(self.show_context_menu)


    def show_context_menu(self, pos):
        index = self.treeview.indexAt(pos)
        if not index.isValid():
            return

        menu = QMenu(self)

        create_file_action = QAction("Create File", self)
        create_file_action.triggered.connect(self.create_file)
        menu.addAction(create_file_action)

        create_dir_action = QAction("Create Directory", self)
        create_dir_action.triggered.connect(self.create_directory)
        menu.addAction(create_dir_action)

        delete_action = QAction("Delete", self)
        delete_action.triggered.connect(self.delete_item)
        menu.addAction(delete_action)

        rename_action = QAction("Rename", self)
        rename_action.triggered.connect(self.rename_item)
        menu.addAction(rename_action)

        menu.exec(self.treeview.viewport().mapToGlobal(pos))

    def recreate_model(self):
        print("should reload")
        #self.model = QFileSystemModel()
        #self.model.setRootPath(QDir.rootPath())
        #self.model.setNameFilters(["*.yml"])
        #self.model.setNameFilterDisables(False)
        #self.treeview.setModel(self.model)

    def create_file(self):
        index = self.treeview.currentIndex()
        if index.isValid() and self.model.isDir(index):
            file_name, ok = QInputDialog.getText(self, "Create File", "Enter file name:")
            if ok:
                file_path = self.model.filePath(index) + "/" + file_name
                with open(file_path, "w") as file:
                    pass  # Create an empty file
                self.recreate_model()

    def create_directory(self):
        index = self.treeview.currentIndex()
        if index.isValid() and self.model.isDir(index):
            dir_name, ok = QInputDialog.getText(self, "Create Directory", "Enter directory name:")
            if ok:
                dir_path = self.model.filePath(index) + "/" + dir_name
                QDir().mkpath(dir_path)
                self.recreate_model()

    def delete_item(self):
        index = self.treeview.currentIndex()
        if index.isValid():
            if self.model.remove(index):
                self.recreate_model()

    def rename_item(self):
        index = self.treeview.currentIndex()
        if index.isValid():
            old_name = self.model.fileName(index)
            new_name, ok =QInputDialog.getText(self, "Create Item", "Enter the name:")
            #new_name, ok = QInputDialog.getText(self, "Rename", "Enter new name:","", old_name)
            if ok:
                new_name = new_name.strip()
                if new_name:
                    dir_path = self.model.filePath(index).rpartition("/")[0]
                    old_path = self.model.filePath(index)
                    new_path = dir_path + "/" + new_name
                    os.rename(old_path,new_path)

                    #if self.model.rename(index, new_path):
                    #    self.recreate_model()



    def _configClicked(self, index):
        model = self.treeview.sender().model()
        if(not model.isDir(index)):
            path = model.filePath(index)
            print(path)

            self.fileClicked.emit(path)


class Window(QWidget):

    def __init__(self):
        super().__init__()

        configLocation = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.ConfigLocation)
        userConfigLocation = configLocation+"/keyboardcontrol"
        #overridea-temp
        userConfigLocation = "/home/vaisakh/vaisakhRoot/programming/python/keyboardcontrol/config/"
        print(configLocation)

        self.configTreeView= ConfigTreeView(userConfigLocation)
        layout = QHBoxLayout()

        layout.addWidget(self.configTreeView)
        label = QLabel("hello")
        layout.addWidget(label)

        self.setLayout(layout)



if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = Window()
    window.show()
    sys.exit(app.exec())
