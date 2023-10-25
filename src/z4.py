
import sys,os
from PyQt6.QtGui import QFileSystemModel,QAction
from PyQt6.QtWidgets import QApplication, QMainWindow, QTreeView, QMenu, QLineEdit, QInputDialog
from PyQt6.QtCore import QDir, QModelIndex, Qt

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


class FileTreeApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("File Tree Viewer")
        self.setGeometry(100, 100, 800, 600)

        self.tree_view = QTreeView(self)
        self.tree_view.setGeometry(10, 10, 780, 580)

        self.setup_model()
        self.setup_ui()

    def setup_model(self):
        self.model = CustomFileSystemModel()
        self.model.setRootPath(QDir.rootPath())
        self.model.setNameFilters(["*.yml"])
        self.model.setNameFilterDisables(False)

    def setup_ui(self):
        self.tree_view.setModel(self.model)
        self.tree_view.setRootIndex(self.model.index("/home/vaisakh/vaisakhRoot/programming/python/keyboardcontrol/"))

        self.tree_view.hideColumn(1)  # Hide size column
        self.tree_view.hideColumn(2)  # Hide type column
        self.tree_view.hideColumn(3)  # Hide date modified column

        self.tree_view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tree_view.customContextMenuRequested.connect(self.show_context_menu)

    def show_context_menu(self, pos):
        index = self.tree_view.indexAt(pos)
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

        menu.exec(self.tree_view.viewport().mapToGlobal(pos))

    def recreate_model(self):
        print("should reload")
        #self.model = QFileSystemModel()
        #self.model.setRootPath(QDir.rootPath())
        #self.model.setNameFilters(["*.yml"])
        #self.model.setNameFilterDisables(False)
        #self.tree_view.setModel(self.model)

    def create_file(self):
        index = self.tree_view.currentIndex()
        if index.isValid() and self.model.isDir(index):
            file_name, ok = QInputDialog.getText(self, "Create File", "Enter file name:")
            if ok:
                file_path = self.model.filePath(index) + "/" + file_name
                with open(file_path, "w") as file:
                    pass  # Create an empty file
                self.recreate_model()

    def create_directory(self):
        index = self.tree_view.currentIndex()
        if index.isValid() and self.model.isDir(index):
            dir_name, ok = QInputDialog.getText(self, "Create Directory", "Enter directory name:")
            if ok:
                dir_path = self.model.filePath(index) + "/" + dir_name
                QDir().mkpath(dir_path)
                self.recreate_model()

    def delete_item(self):
        index = self.tree_view.currentIndex()
        if index.isValid():
            if self.model.remove(index):
                self.recreate_model()

    def rename_item(self):
        index = self.tree_view.currentIndex()
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FileTreeApp()
    window.show()
    sys.exit(app.exec())
