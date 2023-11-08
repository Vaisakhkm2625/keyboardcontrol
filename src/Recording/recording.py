
from PyQt6.QtWidgets import QWidget
from Recording.RecordingUi import Ui_Form


class Recording(QWidget):
    def __init__(self):
        super().__init__()

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        #self.setWindowTitle("title")


