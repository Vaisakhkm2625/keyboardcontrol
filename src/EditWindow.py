from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QApplication,QWidget
from EditProperties import Ui_Form

class EditPropertyWindow(QWidget):

    submitted = pyqtSignal(object)

    def __init__(self,configuration):
        super().__init__()
        self.configuration = configuration
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setValuesUi()
        #print("configuration:",self.configuration)
        #print("configuration:",self.configuration.config)

        self.ui.Submit.clicked.connect(self.onSubmit)

    def setValuesUi(self):

        #name cannot be edited
        self.ui.name_edit.setText(self.configuration.config["name"])
        self.ui.desc_edit.setText(self.configuration.config["desc"])
        self.ui.cmd_edit.setText(self.configuration.config["supported_os"][self.configuration.selectedOs][self.configuration.selectedPlatform]["cmd"])
        self.ui.dependency_edit.setText(self.configuration.config["supported_os"][self.configuration.selectedOs][self.configuration.selectedPlatform]["dependency"])
        self.ui.script_path_edit.setText(self.configuration.config["supported_os"][self.configuration.selectedOs][self.configuration.selectedPlatform]["dependency"])
        self.ui.keybinding_edit.setKeySequence(self.configuration.config["keybinding"])

    def getValuesUi(self):
        self.configuration.config["name"] = self.ui.name_edit.text()
        self.configuration.config["desc"] = self.ui.desc_edit.text()
        #cmd_edit
        self.configuration.config["supported_os"][self.configuration.selectedOs][self.configuration.selectedPlatform]["cmd"] = self.ui.cmd_edit.text()
        #dependency_edit
        self.configuration.config["supported_os"][self.configuration.selectedOs][self.configuration.selectedPlatform]["dependency"] = self.ui.dependency_edit.text()
        #script_path_edit
        self.configuration.config["supported_os"][self.configuration.selectedOs][self.configuration.selectedPlatform]["script_path"] = self.ui.script_path_edit.text()
        self.configuration.config["keybinding"] = self.ui.keybinding_edit.keySequence().toString()

    def onSubmit(self):
        self.getValuesUi()
        self.submitted.emit(self.configuration)
        self.close()

