# Import the core and GUI elements of Qt
import sys
import os

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout, QApplication, QPushButton, QLineEdit, QHBoxLayout, QFileDialog
from pathlib import Path


class SteamPathDialog(QDialog):
    '''
    This class is a dialog to get and display area info.
    '''

    def __init__(self, parent=None, area=None):
        super(SteamPathDialog, self).__init__(parent)

        local_program_folder_path = os.path.normpath(
            os.path.normpath(Path.home()) + "\AppData\Local\SteamAccountManager")
        self.filename = os.path.join(local_program_folder_path, 'steam_path.txt')

        # modify
        self.diag_modify = False  # use the diag as a modify dialog
        self.area_modify = None  # area object to modify
        # qlabel
        self.steampathLabel = QLabel("Steam path: ")
        self.steampathLineEdit = QLineEdit()

        self.errorlabel = QLabel()

        # qlinedit
        self.loginLineEdit = QLineEdit()
        self.passwordLineEdit = QLineEdit()

        # qbutton
        self.buttonchangepath = QPushButton("...")
        self.buttonchangepath.setAutoDefault(False)
        self.buttonchangepath.setDefault(False)
        self.buttonok = QPushButton("Ok")
        self.buttoncancel = QPushButton("Annuler")

        # signal
        self.buttonchangepath.clicked.connect(self.choosepath)
        self.buttonok.clicked.connect(self.choice)
        self.buttoncancel.clicked.connect(self.choice)
        # layout
        self.layout_main = QVBoxLayout()

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.steampathLabel)
        self.layout.addWidget(self.steampathLineEdit)
        self.layout.addWidget(self.buttonchangepath)
        self.layout.addWidget(self.errorlabel)

        self.layout_button = QHBoxLayout()
        self.layout_button.addStretch(1)
        self.layout_button.addWidget(self.buttonok)
        self.layout_button.addWidget(self.buttoncancel)
        self.layout_button.addStretch(1)

        self.layout_main.addLayout(self.layout)
        self.layout_main.addLayout(self.layout_button)

        self.setLayout(self.layout_main)
        self.setWindowTitle("Steam path account")
        self.setFixedSize(self.sizeHint().width() + 100, self.sizeHint().height())
        self.setWindowFlags(Qt.Dialog | Qt.MSWindowsFixedSizeDialogHint)

        self.load_steam_path_file()

    def choice(self):
        if self.sender() == self.buttonok:
            if self.check():
                QDialog.accept(self)
                QDialog.done(self, 1)
        if self.sender() == self.buttoncancel:
            QDialog.reject(self)
            QDialog.done(self, 0)

    def check(self):
        if not self.steampathLineEdit.text():
            self.errorlabel.setText("Steam exe path cannot be empty !")
            return False

        return True

    def result(self):
        self.write_steam_path_file()

        return True

    @staticmethod
    def getWinInfo(parent=None):
        dialog = SteamPathDialog(parent)

        if dialog.exec_() == QDialog.Accepted:
            return dialog.result()

    def choosepath(self):
        fileName, _ = QFileDialog.getOpenFileName(None, "Choose a path for steam exe",
                                                  directory=os.path.normpath(Path.home()), filter="*.exe")
        if fileName:
            self.steampathLineEdit.setText(fileName)

    def write_steam_path_file(self):
        with open(self.filename, "w") as f:
            f.write(self.steampathLineEdit.text())

    def load_steam_path_file(self):
        try:
            f = open(self.filename, "r+")

            for line in f.readlines():
                self.steampathLineEdit.setText(line.replace('\n', ''))

            f.close()

        except FileNotFoundError:
            print("File Not Found Error !")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    diag = SteamPathDialog.getWinInfo(None)
    sys.exit(app.exec_())
