import sys
from PyQt6.QtWidgets import QApplication,QMainWindow, QTreeWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("keyboard")

        treew = QTreeWidget(self)
        treex = QTreeWidget(treew)





app = QApplication(sys.argv)

window = MainWindow()
window.show()

sys.exit(app.exec())

