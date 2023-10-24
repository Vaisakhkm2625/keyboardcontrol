from PyQt6.QtWidgets import QApplication,QWidget
from EditProperties import Ui_Form


class EditPropertyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)



    #class ItemPropertyUi():
    #    def __init__(self,ui,configuration):
    #
    #        self.configuration = configuration
    #        self.configPath = ""
    #        self.ui = ui
    #
    #        #self.setValues("");
    #
    #    def setValuesUi(self):
    #        self.setDescUi()
    #        self.setNameUi()
    #        self.setKeybinding()
    #
    #    def getValuesUi(self):
    #        self.getDescUi()
    #        self.getNameUi()
    #        self.getKeybinding()
    #
    #    def setDescUi(self):
    #        desc = self.configuration.config["desc"]
    #        self.ui.desc.setText(desc)
    #
    #    def setNameUi(self):
    #        name = self.configuration.config["name"]
    #        self.ui.name.setText(name)
    #
    #    def setKeybinding(self):
    #    #self.ui.name.setText(configuration.config[self.page]["actions"][action]["name"])
    #        keybinding = self.configuration.config["keybinding"]
    #        self.ui.keySequence.setKeySequence(keybinding)
    #
    #    def getDescUi(self):
    #        self.configuration.config["desc"] = self.ui.desc.text
    #
    #    def getNameUi(self):
    #        name = self.configuration.config["name"] = self.ui.desc.text
    #        self.ui.name.setText(name)
    #
    #    def getKeybinding(self):
    #    #self.ui.name.setText(configuration.config[self.page]["actions"][action]["name"])
    #    #   keybinding = configuration.config["keybinding"]
    #    #   self.ui.keySequence.setKeySequence(keybinding)
    #        return "Ctrl+Shift+j"
