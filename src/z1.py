
import sys
from PyQt6.QtGui import QFileSystemModel
from PyQt6.QtWidgets import QApplication, QMainWindow, QTreeView
from PyQt6.QtCore import Qt

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

def main():
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setGeometry(100, 100, 800, 600)

    treeView = QTreeView(window)
    customModel = CustomFileSystemModel()
    customModel.setRootPath('')
    treeView.setModel(customModel)
    treeView.setRootIndex(customModel.index(''))  # Set the root index to the desired directory

    # Hide all columns except the first one
    for column in range(1, customModel.columnCount()):
        treeView.setColumnHidden(column, True)

    window.setCentralWidget(treeView)
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
