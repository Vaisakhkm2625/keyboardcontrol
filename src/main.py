import sys,yaml
from PyQt6.QtWidgets import QApplication,QMainWindow, QWidget

from AppMainUi import Ui_MainWindow


class Config():
    def __init__(self):

        self.config_path = "/home/vaisakh/.config/keyboardcontrol/default.yml"


        with open(self.config_path) as file:
            self.config = yaml.safe_load(file)

        self.os=sys.platform
        self.platform="hyprland"


# TODO: connect with signels and slots and make this local variable
configuration = Config()
        

class Application(QApplication):

    def __init__(self, argv):
        super().__init__(argv)

        self.window = MainWindow()
        self.window.show()



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("keyboard")


        #self.sidenav = SideNav(self.ui.treeWidget)

        self.ui.treeWidget.clicked.connect(self.setBodyItem)

        #self.itemViewer = ItemViewer(self.ui,"general","screenshot")
        #self.itemViewer.setValuesUi("screenshot")


        #treew = QTreeWidget(self)
        #treex = QTreeWidget(treew)

        #self.show()

    def setBodyItem(self,sideNavTreeItem):
        print(sideNavTreeItem)



class ItemViewer():
    def __init__(self,ui,page,action):

        self.ui = ui
        self.page = page
        self.action = action

        #self.setValues("");

    def setAction(self,action):
        self.action = action

    def setValuesUi(self,action):
        self.setDescUi()
        self.setNameUi()
        self.setKeybinding()

    def setDescUi(self):
        desc = configuration.config[self.page]["actions"][self.action]["desc"]
        self.ui.desc.setText(desc)

    def setNameUi(self):
        name = configuration.config[self.page]["actions"][self.action]["name"]
        self.ui.name.setText(name)

    def setKeybinding(self):
    #self.ui.name.setText(configuration.config[self.page]["actions"][action]["name"])
        self.ui.keySequence.setKeySequence("Ctrl+P")




if __name__ == "__main__":
    app = Application(sys.argv)
    sys.exit(app.exec())
