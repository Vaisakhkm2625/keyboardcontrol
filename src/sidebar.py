import sys
import yaml
from PyQt6.QtWidgets import QApplication, QWidget,QTreeWidget, QTreeWidgetItem, QVBoxLayout,QHBoxLayout, QPushButton, QSpacerItem,QLabel


config_path = "/home/vaisakh/.config/keyboardcontrol/default.yml"

with open(config_path) as file:
    config = yaml.safe_load(file)

os="linux"
platform="hyprland"


class SideNavTreeItem(QTreeWidgetItem):
    def __init__(self,tree,key):
        super().__init__(tree)

        self.key = key;


class MainUi(QWidget):
    def __init__(self):
        super().__init__()

        button = QPushButton("hello",self)

        self.name = QLabel("name",self)

        layout = QHBoxLayout()
        layout.addWidget(button)
        layout.addWidget(self.name)
        self.setLayout(layout)

    def setName(self,name_in):
        self.name.setText(name_in)


class Widget(QWidget):
    def __init__(self):
        super().__init__()


        self.main_layout = QHBoxLayout()

        tree = QTreeWidget()
        tree.setColumnCount(1)
        tree.itemClicked.connect(self.printDetails)


        general = QTreeWidgetItem(tree)
        general.setText(0,"General utilities")

        for k,v in config["general"].items():
            generalAction= SideNavTreeItem(general,k)
            generalAction.setText(0,v["name"])

        self.mainui = MainUi()
        self.main_layout.addWidget(tree)
        self.main_layout.addWidget(self.mainui)

        self.setLayout(self.main_layout)

    def printDetails(self,k):
        print(k.key)
        self.mainui.name.setText(k.key)
        #print(config["general"][k]['name'])
    #    print(config["general"][k][os][platform]['cmd'])


app = QApplication(sys.argv)

widget = Widget()
widget.show()
sys.exit(app.exec())
