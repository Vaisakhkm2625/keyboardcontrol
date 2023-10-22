import sys
from PyQt6.QtWidgets import QApplication,QMainWindow, QTreeWidget

from AppMainWindow import Ui_MainWindow


class Application(QApplication):

    def __init__(self, argv):
        super().__init__(argv)

        window = MainWindow()
        window.show()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()


        self.setWindowTitle("keyboard")

        treew = QTreeWidget(self)
        treex = QTreeWidget(treew)



if __name__ == "__main__":
    app = Application(sys.argv)
    sys.exit(app.exec())
