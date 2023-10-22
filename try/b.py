import sys
import yaml
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QFormLayout, QPushButton, QTextEdit, QLabel, QFileDialog,QInputDialog,QVBoxLayout

class YamlEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('YAML File Editor')
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.label = QLabel('Edit YAML Data:')
        self.layout.addWidget(self.label)

        self.text_edit = QTextEdit()
        self.layout.addWidget(self.text_edit)

        self.load_button = QPushButton('Load YAML File')
        self.layout.addWidget(self.load_button)

        self.save_button = QPushButton('Save YAML File')
        self.layout.addWidget(self.save_button)

        self.form_layout = QFormLayout()
        self.layout.addLayout(self.form_layout)

        self.add_field_button = QPushButton('+ Add Field')
        self.add_field_button.clicked.connect(self.add_field)
        self.layout.addWidget(self.add_field_button)

        self.load_button.clicked.connect(self.load_yaml)
        self.save_button.clicked.connect(self.save_yaml)

        self.setLayout(layout)

        self.data = {}

    def load_yaml(self):
        dialog = QFileDialog()
        options = QFileDialog.options(dialog)
        #options |= QFileDialog.readOnly

        file_path, _ = QFileDialog.getOpenFileName(self, "Open YAML File", "", "YAML Files (*.yaml *.yml);;All Files (*)", options=options)

        if file_path:
            with open(file_path, 'r') as file:
                self.data = yaml.safe_load(file)
                self.update_form_layout()

    def save_yaml(self):
        dialog = QFileDialog()
        options = QFileDialog.options(dialog)
        #options |= QFileDialog.ReadOnly

        file_path, _ = QFileDialog.getSaveFileName(self, "Save YAML File", "", "YAML Files (*.yaml *.yml);;All Files (*)", options=options)

        if file_path:
            self.read_form_layout()
            with open(file_path, 'w') as file:
                yaml.dump(self.data, file, default_flow_style=False)

    def add_field(self):
        key, ok = QInputDialog.getText(self, "Add Field", "Enter Field Name:")
        if ok and key:
            self.form_layout.addRow(key, QTextEdit())

    def update_form_layout(self):
        # Clear existing fields
        for i in reversed(range(self.form_layout.count())):
            widget = self.form_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        # Populate with dapyqt program for updating a yaml fileta
        for key, value in self.data.items():
            self.form_layout.addRow(key, QTextEdit(str(value)))

    def read_form_layout(self):
        self.data = {}
        for i in range(self.form_layout.count()):
            item = self.form_layout.itemAt(i)
            if item.widget() and isinstance(item.widget(), QTextEdit):
                key = self.form_layout.labelForField(item.widget())#.text()
                #value = item.widget().toPlainText()
                #self.data[key] = value

def main():
    app = QApplication(sys.argv)
    window = YamlEditor()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
