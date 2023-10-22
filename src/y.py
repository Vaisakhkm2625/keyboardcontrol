
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout

class MainUi(QWidget):
    def __init__(self):
        super().__init__()

        # Create the "hello" button and add it directly to the MainUi widget
        button = QPushButton("hello", self)

class Widget(QWidget):
    def __init__(self):
        super().__init__()

        # Create a layout for the Widget
        self.main_layout = QVBoxLayout()

        # Create the "hi" button and add it to the layout
        button = QPushButton("hi")
        self.main_layout.addWidget(button)

        # Create the MainUi widget and add it to the layout
        mainui = MainUi()
        self.main_layout.addWidget(mainui)

        # Set the layout for the Widget
        self.setLayout(self.main_layout)

if __name__ == '__main__':
    app = QApplication([])
    widget = Widget()
    widget.show()
    app.exec()
