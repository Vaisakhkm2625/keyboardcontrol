import sys,yaml
from PyQt6.QtCore import QStandardPaths, pyqtSignal
from PyQt6.QtWidgets import QApplication, QHBoxLayout,QMainWindow, QWidget

from AppMainUi import Ui_MainWindow
from sidebar2 import ConfigTreeView

from EditWindow import EditPropertyWindow

class Config():
    def __init__(self):

        configLocation = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.ConfigLocation)
        self.userConfigPath = configLocation+"/keyboardcontrol"
        #override
        self.userConfigPath = "/home/vaisakh/vaisakhRoot/programming/python/keyboardcontrol/config/"

        self.currentConfigPath="";
        self.config = {}
        print(self.userConfigPath)


        self.os=sys.platform
        self.platform="hyprland"

    def setCurrentConfig(self,path):
        self.currentConfigPath = path
        with open(self.currentConfigPath) as file:
            self.config = yaml.safe_load(file)
            print(self.config)


# TODO: connect with signels and slots and make this local variable
configuration = Config()
        

class Application(QApplication):

    def __init__(self, argv):
        super().__init__(argv)

        self.window = MainWindow()
        self.window.show()


class MainWindow(QMainWindow):

    edit_signel = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("keyboard")

        self.configTreeView = ConfigTreeView(configuration.userConfigPath)

        layout = QHBoxLayout(self.ui.filetree_wrapper)
        layout.addWidget(self.configTreeView)

        self.configTreeView.fileClicked.connect(self.setBodyItem)

        self.itempropertybody = ItemPropertyUi(self.ui)

        self.ui.edit_properties_button.clicked.connect(self.editProperies)



    def setBodyItem(self,filepath):
        print("setBodyItem",filepath)
        configuration.setCurrentConfig(filepath)
        self.itempropertybody.setValuesUi()

    def editProperies(self):
        print("hello")

        self.editiwindow = EditPropertyWindow() 
        self.editiwindow.show()


class ItemPropertyUi():

    def __init__(self,ui):

        self.configPath = ""
        self.ui = ui

        #self.setValues("");

    def setValuesUi(self):
        self.setDescUi()
        self.setNameUi()
        self.setKeybinding()

    def getValuesUi(self):
        self.getDescUi()
        self.getNameUi()
        self.getKeybinding()

    def setDescUi(self):
        desc = configuration.config["desc"]
        self.ui.desc.setText(desc)

    def setNameUi(self):
        name = configuration.config["name"]
        self.ui.name.setText(name)

    def setKeybinding(self):
    #self.ui.name.setText(configuration.config[self.page]["actions"][action]["name"])
        keybinding = configuration.config["keybinding"]
        self.ui.keySequence.setKeySequence(keybinding)

    def getDescUi(self):
        configuration.config["desc"] = self.ui.desc.text

    def getNameUi(self):
        name = configuration.config["name"] = self.ui.desc.text
        self.ui.name.setText(name)

    def getKeybinding(self):
    #self.ui.name.setText(configuration.config[self.page]["actions"][action]["name"])
    #   keybinding = configuration.config["keybinding"]
    #   self.ui.keySequence.setKeySequence(keybinding)
        return "Ctrl+Shift+j"





if __name__ == "__main__":
    app = Application(sys.argv)
    sys.exit(app.exec())
