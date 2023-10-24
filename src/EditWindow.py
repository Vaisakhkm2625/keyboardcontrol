from PyQt6.QtWidgets import QApplication,QWidget
from EditProperties import Ui_Form

class EditPropertyWindow(QWidget):
    def __init__(self,configuration):
        super().__init__()
        self.configuration = configuration
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.itemPropertyUi = ItemPropertyUi(self.ui,self.configuration)
        self.itemPropertyUi.setValuesUi()

class ItemPropertyUi():
    def __init__(self,ui,configuration):

        self.configuration = configuration
        print("configuration:",self.configuration)
        print("configuration:",self.configuration.config)

        self.configPath = ""
        self.ui = ui

        #self.ui.save

        #self.setValues("");

    def setValuesUi(self):
        print("desc:",self.configuration.config["desc"])
        self.ui.desc_edit.setText(self.configuration.config["desc"])
        #name cannot be edited
        self.ui.name_edit.setText(self.configuration.config["name"])
        self.ui.keybinding_edit.setKeySequence(self.configuration.config["keybinding"])

    def getValuesUi(self):
        self.configuration.config["desc"] = self.ui.desc_edit.text
        self.configuration.config["name"] = self.ui.name_edit.text
        self.configuration.config["keybinding"] = self.ui.keybinding_edit.keySequence().toString()

