from io import open_code
import sys,yaml
from PyQt6.QtCore import QStandardPaths, pyqtSignal
from PyQt6.QtWidgets import QApplication, QHBoxLayout,QMainWindow, QWidget

from AppMainUi import Ui_MainWindow
from Sidebar import ConfigTreeView

from Recording import Recording

from EditWindow import EditPropertyWindow

from keyboardCapture import KeyboardController

from qt_material import apply_stylesheet


class Config():
    def __init__(self):

        configLocation = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.ConfigLocation)
        self.userConfigPath = configLocation+"/keyboardcontrol"
        #override
        #self.userConfigPath = "/home/vaisakh/vaisakhRoot/programming/python/keyboardcontrol/config/"
        self.userConfigPath = "../config/"

        self.currentConfigPath="";
        self.config = {}
        #print(self.userConfigPath)

        self.os=sys.platform
        self.selectedOs=sys.platform
        self.platform=sys.platform
        #self.selectedPlatform="hyprland"
        self.selectedPlatform="windows10"

    def setCurrentConfig(self,path):
        self.currentConfigPath = path
        with open(self.currentConfigPath) as file:
            self.config = yaml.safe_load(file)
            #print(self.config)

    def saveConfig(self):
        print("saving")
        print(yaml.dump(self.config))

        with open(self.currentConfigPath, 'w') as  file:
            yaml.dump(self.config,file, default_flow_style=False)


# TODO: connect with signels and slots and make this local variable
configuration = Config()
        

class Application(QApplication):

    def __init__(self, argv):
        super().__init__(argv)

        apply_stylesheet(self, theme='dark_teal.xml')
        self.window = MainWindow()
        self.window.show()


class MainWindow(QMainWindow):

    edit_signel = pyqtSignal()
    #os_selection_selection_changed = pyqtSignal()
    #platform_selection_selection_changed = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.keyboard = KeyboardController(configuration.os,configuration.platform,configuration.userConfigPath)

        self.setWindowTitle("keyboard")

        self.configTreeView = ConfigTreeView(configuration.userConfigPath)
        layout = QHBoxLayout(self.ui.filetree_wrapper)
        layout.addWidget(self.configTreeView)

        self.configTreeView.fileClicked.connect(self.setBodyItem)

        #self.itempropertybody = ItemPropertyUi(self.ui)
        self.ui.edit_properties_button.clicked.connect(self.editProperies)

        self.ui.keybinding.keySequenceChanged.connect(self.getKeybinding)
        self.ui.os_combobox.activated.connect(self.onOSComboboxChanged)
        self.ui.platform_combobox.activated.connect(self.onPlatformComboboxChanged)
        self.ui.save_button.clicked.connect(self.onSaveButtonPressed)
        self.ui.settings_button.clicked.connect(self.onSettingsButtonClicked)

        self.ui.reset_button.clicked.connect(self.onResetButtonPressed)

        self.ui.apply_button.clicked.connect(self.onApplyButtonPressed)

        rec =  Recording()

        self.ui.stackedWidget.addWidget(rec)
        self.ui.stackedWidget.setCurrentWidget(rec)


    def onSaveButtonPressed(self):
        configuration.saveConfig()


    def onResetButtonPressed(self):
        self.setBodyItem(configuration.currentConfigPath)


    def onApplyButtonPressed(self):
        self.keyboard.setup()
        self.keyboard.run()


    def setBodyItem(self,filepath):
        print("setBodyItem",filepath)
        configuration.setCurrentConfig(filepath)
        self.ui.stackedWidget.setCurrentWidget(self.ui.general_page)
        self.setValuesUi()

    def refreshUi(self,config):
        configuration = config
        print(configuration)
        print(configuration.config)
        self.setValuesUi()



    def editProperies(self):
        #print(configuration.config)
        self.editwindow = EditPropertyWindow(configuration) 
        self.editwindow.show()
        self.editwindow.submitted.connect(self.refreshUi)

    def setValuesUi(self):
        self.setDescUi()
        self.setNameUi()
        self.setKeybinding()
        self.setOSCombobox()
        self.setPlatformCombobox()

    #def getValuesUi(self):
        #self.getDescUi()
        #self.getNameUi()
        #self.getKeybinding()

    def setDescUi(self):
        desc = configuration.config["desc"]
        self.ui.desc.setText(desc)

    def setNameUi(self):
        name = configuration.config["name"]
        self.ui.name.setText(name)

    def setKeybinding(self):
        keybinding = configuration.config["keybinding"]
        self.ui.keybinding.setKeySequence(keybinding)

    def getKeybinding(self):
        configuration.config["keybinding"] = self.ui.keybinding.keySequence().toString()
        
    def setOSCombobox(self):
        osList = list(configuration.config["supported_os"])
        self.ui.os_combobox.clear()
        self.ui.os_combobox.addItems(osList)
        # potential event-callback recurrsion
        configuration.selectedOs = configuration.os
        configuration.selectedPlatform = configuration.platform
        if configuration.os in osList:
            self.ui.os_combobox.setCurrentIndex(osList.index(configuration.os))
        else:
            self.ui.os_combobox.setPlaceholderText("os not supported")
            self.ui.os_combobox.setCurrentIndex(-1)

    def changeOSComboboxSelection(self):
        configuration.selectedOs = self.ui.os_combobox.currentText()

    def setPlatformCombobox(self):
        self.ui.platform_combobox.clear()
        if configuration.selectedOs in list(configuration.config["supported_os"]):
            platformsList = list(configuration.config["supported_os"][configuration.selectedOs])
            self.ui.platform_combobox.addItems(platformsList)
            if configuration.selectedPlatform in platformsList:
                self.ui.platform_combobox.setCurrentIndex(platformsList.index(configuration.selectedPlatform))
            else:
                self.ui.platform_combobox.setPlaceholderText("platform supported")
                self.ui.platform_combobox.setCurrentIndex(-1)
        else:
            self.ui.platform_combobox.setPlaceholderText("os not supported")
            self.ui.platform_combobox.setCurrentIndex(-1)

    def changePlatformComboboxSelection(self):
        platformsList = list(configuration.config["supported_os"][configuration.selectedOs])
        configuration.selectedPlatform = platformsList[0]
        #configuration.platform = self.ui.platform_combobox.currentText()

        self.setPlatformCombobox()


    def getOSComboboxSelection(self):
        configuration.selectedOs = self.ui.os_combobox.currentText()
        #addItems(list(configuration.config["supported_os"]))

    def getPlatformComboboxSelection(self):
        configuration.platform = self.ui.platform_combobox.currentText()
        #addItems(list(configuration.config["supported_os"]))

    def onOSComboboxChanged(self):
        print("OSComboboxChanged")
        self.getOSComboboxSelection()
        self.changePlatformComboboxSelection()

    def onPlatformComboboxChanged(self):
        print("PlatformComboboxChanged")
        configuration.selectedPlatform= self.ui.platform_combobox.currentText()
        #self.setValuesUi()

    def onSettingsButtonClicked(self):
        print("StackViewChaged")
        self.ui.stackedWidget.setCurrentWidget(self.ui.settings_page)
        self.ui.config_path.setText(configuration.userConfigPath)

        


    # def getDescUi(self):
    #     configuration.config["desc"] = self.ui.desc.text
    #
    # def getNameUi(self):
    #     name = configuration.config["name"] = self.ui.desc.text
    #     self.ui.name.setText(name)



if __name__ == "__main__":
    app = Application(sys.argv)
    sys.exit(app.exec())
