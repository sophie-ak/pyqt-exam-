import os
import re
from PySide6 import QtWidgets
from ui import finder_ui


class Finder(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = finder_ui.Ui_Form()
        self.ui.setupUi(self)

        # Button actions
        self.ui.pushButton.clicked.connect(self.browse_closed)
        self.ui.pushButton_2.clicked.connect(self.search_files)

    # BUTTON ACTIONS
    def browse_folders(self):
        self.ui.lineEdit.clear()
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Enter the folder")
        for _ in os.listdir(directory):
            self.ui.lineEdit.setText(directory)

    def browse_closed(self):
        self.browse_folders()
        self.str_search()

    def search_files(self):
        if self.ui.comboBox.currentText() == "String":
            self.str_search()
        elif self.ui.comboBox.currentText() == "Bytes":
            self.byte_sign_search()
        else:
            self.binary_sign_search()

    # SEARCH TYPES
    def str_search(self):
        start_folder = self.ui.lineEdit.text()
        search = self.ui.lineEdit_2.text()
        self.ui.listWidget.clear()

        for root, dirs, files in os.walk(start_folder):
            for file in files:
                file_path: str = os.path.join(root, file)
                if file_path.endswith(search):
                    directories = os.path.abspath(file_path)
                    self.ui.listWidget.addItem(directories)

    def byte_sign_search(self):
        start_folder = self.ui.lineEdit.text()
        search = self.ui.lineEdit_2.text()
        self.ui.listWidget.clear()

        for root, dirs, files in os.walk(start_folder):
            for file in files:
                file_path: str = os.path.join(root, file)
                with open(file_path, "rb") as f:
                    if search.encode('utf-8') in f.read():
                        directories = os.path.abspath(file_path)
                        self.ui.listWidget.addItem(directories)

    def binary_sign_search(self):
        start_folder = self.ui.lineEdit.text()
        search = self.ui.lineEdit_2.text()
        self.ui.listWidget.clear()

        for root, dirs, files in os.walk(start_folder):
            for file in files:
                file_path: str = os.path.join(root, file)
                with open(file_path, "rb"):
                    search_file = re.compile(search)
                    search_file.findall(file)
                    if search_file.findall(file) is not None:
                        directories = os.path.abspath(file_path)
                        self.ui.listWidget.addItem(directories)
                    else:
                        self.ui.listWidget.addItem("None")


if __name__ == "__main__":
    app = QtWidgets.QApplication()
    w = Finder()
    w.show()
    app.exec()
