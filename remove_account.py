# Import the core and GUI elements of Qt
import sys
import os
from pathlib import Path
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QLabel, QGridLayout, QApplication, QPushButton, QComboBox


class RemoveAccountDialog(QDialog):
    '''
    This class is a dialog to get and display area info.
    '''

    def __init__(self, parent=None, area=None):
        super(RemoveAccountDialog, self).__init__(parent)

        local_program_folder_path = os.path.normpath(
            os.path.normpath(Path.home()) + "\AppData\Local\SteamAccountManager")
        self.filename = os.path.join(local_program_folder_path, 'accounts.txt')
        self.account_dic = {}
        # modify
        self.diag_modify = False  # use the diag as a modify dialog
        self.area_modify = None  # area object to modify
        # qlabel
        self.accountLabel = QLabel("Account: ")

        # qcombobox
        self.accountCombobox = QComboBox()

        # qbutton
        self.button_remove = QPushButton("Remove selected account")
        self.button_remove.setDefault(False)
        self.button_remove.setAutoDefault(False)
        self.button_remove.clicked.connect(self.remove_selected_account)
        self.buttonok = QPushButton("Ok")
        self.buttoncancel = QPushButton("Annuler")

        # signal
        self.buttonok.clicked.connect(self.choice)
        self.buttoncancel.clicked.connect(self.choice)

        # layout
        self.layout = QGridLayout()
        self.layout.addWidget(self.accountLabel, 0, 0)

        self.layout.addWidget(self.accountCombobox, 0, 1)

        self.layout.addWidget(self.button_remove,1,0)

        self.layout.addWidget(self.buttonok, 5, 0)
        self.layout.addWidget(self.buttoncancel, 5, 1)

        self.setLayout(self.layout)
        self.setWindowTitle("Remove account")
        self.setFixedSize(self.sizeHint().width() + 100, self.sizeHint().height())
        self.setWindowFlags(Qt.Dialog | Qt.MSWindowsFixedSizeDialogHint)

        self.load_account_file()
        self.load_combo_box()

    def choice(self):
        if self.sender() == self.buttonok:
            if self.check():
                QDialog.accept(self)
                QDialog.done(self, 1)
        if self.sender() == self.buttoncancel:
            QDialog.reject(self)
            QDialog.done(self, 0)

    def check(self):

        return True

    def result(self):

        return True

    def remove_selected_account(self):
        print("remove selected account")
        to_be_removed = self.account_dic[self.accountCombobox.currentText()]
        to_be_removed = to_be_removed[0] + " " + to_be_removed[1]

        with open(self.filename, "r") as f:
            lines = f.readlines()
        with open(self.filename, "w") as f:
            for line in lines:
                if not to_be_removed in line:
                    f.write(line)

    @staticmethod
    def getWinInfo(parent=None):
        dialog = RemoveAccountDialog(parent)

        if dialog.exec_() == QDialog.Accepted:
            return dialog.result()

    def load_account_file(self):
        self.account_dic = {}

        f = open(self.filename, "r+")

        for line in f.readlines():
            username, password = line.split(' ')
            self.account_dic[username] = [username, password]

        f.close()

    def load_combo_box(self):
        if len(self.account_dic) == 0:
            self.accountCombobox.addItem("No account(s) registered !")
            self.button_remove.setDisabled(True)
        for key in self.account_dic.keys():
            self.accountCombobox.addItem(key)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    diag = RemoveAccountDialog.getWinInfo(None)
    sys.exit(app.exec_())
