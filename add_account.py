# Import the core and GUI elements of Qt
import sys
import os
from pathlib import Path
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QLabel, QGridLayout, QApplication, QPushButton, QLineEdit


class AddAccountDialog(QDialog):
    '''
    This class is a dialog to get and display area info.
    '''

    def __init__(self, parent=None, area=None):
        super(AddAccountDialog, self).__init__(parent)

        local_program_folder_path = os.path.normpath(os.path.normpath(Path.home()) + "\AppData\Local\SteamAccountManager")
        self.filename = os.path.join(local_program_folder_path, 'accounts.txt')
        # modify
        self.diag_modify = False  # use the diag as a modify dialog
        self.area_modify = None  # area object to modify
        # qlabel
        self.loginLabel = QLabel("Login: ")
        self.passwordLabel = QLabel("Password: ")

        self.errorlabel = QLabel()

        # qlinedit
        self.loginLineEdit = QLineEdit()
        self.passwordLineEdit = QLineEdit()

        # qbutton
        self.buttonok = QPushButton("Ok")
        self.buttoncancel = QPushButton("Annuler")

        # signal
        self.buttonok.clicked.connect(self.choice)
        self.buttoncancel.clicked.connect(self.choice)

        # layout
        self.layout = QGridLayout()
        self.layout.addWidget(self.loginLabel, 0, 0)
        self.layout.addWidget(self.loginLineEdit, 0, 1)
        self.layout.addWidget(self.passwordLabel, 1, 0)
        self.layout.addWidget(self.passwordLineEdit, 1, 1)

        self.layout.addWidget(self.errorlabel, 4, 1)

        self.layout.addWidget(self.buttonok, 5, 0)
        self.layout.addWidget(self.buttoncancel, 5, 1)

        self.setLayout(self.layout)
        self.setWindowTitle("Add account")
        self.setFixedSize(self.sizeHint().width() + 100, self.sizeHint().height())
        self.setWindowFlags(Qt.Dialog | Qt.MSWindowsFixedSizeDialogHint)

    def choice(self):
        if self.sender() == self.buttonok:
            if self.check():
                QDialog.accept(self)
                QDialog.done(self, 1)
        if self.sender() == self.buttoncancel:
            QDialog.reject(self)
            QDialog.done(self, 0)

    def check(self):
        if not self.loginLineEdit.text():
            self.errorlabel.setText("Le champ nom ne peut pas être vide !")
            return False

        if not self.passwordLineEdit.text():
            self.errorlabel.setText("Le champ code ne peut pas être vide !")
            return False

        return True

    def result(self):

        fic = open(self.filename, 'at')

        line = self.loginLineEdit.text() + " " + self.passwordLineEdit.text() + "\n"

        fic.write(line)
        fic.close()

        return True

    @staticmethod
    def getWinInfo(parent=None):
        dialog = AddAccountDialog(parent)

        if dialog.exec_() == QDialog.Accepted:
            return dialog.result()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    diag = AddAccountDialog.getWinInfo(None)
    sys.exit(app.exec_())
