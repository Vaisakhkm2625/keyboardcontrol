import sys,yaml
from PyQt6.QtWidgets import QApplication,QMainWindow, QTreeWidget, QTreeWidgetItem, QWidget

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


        self.sidenav = SideNav(self.ui.treeWidget)

        self.ui.treeWidget.clicked.connect(self.setBodyItem)

        #self.itemViewer = ItemViewer(self.ui,"general","screenshot")
        #self.itemViewer.setValuesUi("screenshot")


        #treew = QTreeWidget(self)
        #treex = QTreeWidget(treew)

        #self.show()

    def setBodyItem(self,sideNavTreeItem):
        print(sideNavTreeItem)



class SideNavTreeItem(QTreeWidgetItem):
    def __init__(self,tree,key):
        super().__init__(tree)

        self.key = key;


class SideNav(QWidget):
    def __init__(self,parent):
        super().__init__()


        #print(configuration.config)
        self.side_nav_tree = parent

        self.setTree("general")
        self.setTree("applications")

        # general = SideNavTreeItem(side_nav_tree,"general")
        # general.setText(0,"General utilities")

        # for k,v in config["general"].items():
        #     generalAction= SideNavTreeItem(general,k)
        #     generalAction.setText(0,v["name"])


    def setTree(self,item_key):

        item = SideNavTreeItem(self.side_nav_tree,item_key)
        item.setText(0,configuration.config[item_key]["name"])

        for k,v in configuration.config[item_key]["actions"].items():
            itemAction= SideNavTreeItem(item,k)
            itemAction.setText(0,v["name"])


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
