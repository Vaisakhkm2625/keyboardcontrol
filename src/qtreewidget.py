import sys
from PyQt6.QtWidgets import QApplication, QTreeWidget, QTreeWidgetItem

app = QApplication(sys.argv)

tree = QTreeWidget()
tree.setColumnCount(1)

root = QTreeWidgetItem(tree)
root.setText(0, "Root")

child1 = QTreeWidgetItem(root)
child1.setText(0, "Child 1")

child2 = QTreeWidgetItem(root)
child2.setText(0, "Child 2")

tree.expandAll()

tree.show()

sys.exit(app.exec())

