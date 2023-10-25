import sys
from PyQt6.QtGui import QFileSystemModel
from PyQt6.QtWidgets import QApplication, QMainWindow, QTreeView
from PyQt6.QtCore import QDir, QModelIndex

class FileTreeApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("File Tree Viewer")
        self.setGeometry(100, 100, 800, 600)

        self.tree_view = QTreeView(self)
        self.tree_view.setGeometry(10, 10, 780, 580)

        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.rootPath())
        self.model.setNameFilters(["*.yml"])
        self.model.setNameFilterDisables(False)

        self.tree_view.setModel(self.model)
        self.tree_view.setRootIndex(self.model.index(QDir.rootPath()))

        self.tree_view.hideColumn(1)  # Hide size column
        self.tree_view.hideColumn(2)  # Hide type column
        self.tree_view.hideColumn(3)  # Hide date modified column

        self.tree_view.doubleClicked.connect(self.on_item_double_clicked)

    def on_item_double_clicked(self, index):
        if not self.model.isDir(index):
            file_path = self.model.filePath(index)
            print(f"Double-clicked on file: {file_path}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FileTreeApp()
    window.show()
    sys.exit(app.exec())
