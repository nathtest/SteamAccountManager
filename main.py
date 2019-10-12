#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys
import ctypes
from pathlib import Path
import add_account
import remove_account
import SteamThread
import steam_path

# Import the core and GUI elements of Qt
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow,QAction,QWidget,QVBoxLayout,QPushButton,QComboBox,QMessageBox,QLabel,QApplication

# to allow windows icon task bar
myappid = 'nath.app.SAM'  # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

local_program_folder_path = os.path.normpath(os.path.normpath(Path.home()) + "\AppData\Local\SteamAccountManager")

if not os.path.exists(local_program_folder_path):
    os.mkdir(local_program_folder_path)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.mainGUI = MainGui(self)
        self.setCentralWidget(self.mainGUI)

        self.setMinimumSize(QSize(300, 100))
        self.setWindowTitle('Steam Account Manager')
        self.setWindowIcon(QIcon(resource_path("resource/steam-icon.png")))

        self.closeEvent = self.mainGUI.closeEvent  # close event is handled in mainGUI

        # menu action
        self.quitAction = QAction("&Quit", self)
        self.quitAction.setShortcut("Ctrl+Q")
        self.quitAction.setStatusTip('Quit Steam Account Manager')
        self.quitAction.triggered.connect(self.close)
        self.quitAction.setIcon(QIcon(resource_path("resource/close-icon.png")))

        self.addAction = QAction("&Add Account", self)
        self.addAction.setShortcut("Ctrl+A")
        self.addAction.setStatusTip('Add Account')
        self.addAction.triggered.connect(self.mainGUI.add_account)
        self.addAction.setIcon(QIcon(resource_path("resource/add-icon.png")))

        self.removeAction = QAction("&Remove Account", self)
        self.removeAction.setShortcut("Ctrl+R")
        self.removeAction.setStatusTip('Remove Account')
        self.removeAction.triggered.connect(self.mainGUI.remove_account)
        self.removeAction.setIcon(QIcon(resource_path("resource/delete-icon.png")))

        self.pathAction = QAction("&Change Steam path", self)
        self.pathAction.setShortcut("Ctrl+C")
        self.pathAction.setStatusTip('Change Steam path')
        self.pathAction.triggered.connect(self.mainGUI.change_steam_path)
        self.pathAction.setIcon(QIcon(resource_path("resource/steam-icon.png")))

        self.aboutAction = QAction("&About", self)
        self.aboutAction.setShortcut("Ctrl+B")
        self.aboutAction.setStatusTip('About')
        self.aboutAction.triggered.connect(self.mainGUI.aboutPopUp)
        self.aboutAction.setIcon(QIcon(resource_path("resource/about-icon.png")))

        self.statusBar()

        # menu bar
        mainMenu = self.menuBar()

        fileMenu = mainMenu.addMenu('&Tools')

        fileMenu.addAction(self.addAction)
        fileMenu.addAction(self.removeAction)
        fileMenu.addAction(self.pathAction)
        fileMenu.addAction(self.aboutAction)
        fileMenu.addAction(self.quitAction)

        self.show()


class MainGui(QWidget):

    def __init__(self, parent):
        super(MainGui, self).__init__(parent)

        # grid layout
        self.main_vlayout = QVBoxLayout(self)
        self.setLayout(self.main_vlayout)

        # button
        self.connectButton = QPushButton("Launch Steam")
        self.connectButton.setIcon(QIcon(resource_path("resource/steam-icon.png")))

        self.qcombobox_account = QComboBox()
        # signal
        self.connectButton.clicked.connect(self.connect)

        # gui layout
        self.main_vlayout.addWidget(self.qcombobox_account)
        self.main_vlayout.addWidget(self.connectButton)

        # model
        self.account_dic = {}
        self.filename = os.path.join(local_program_folder_path, 'accounts.txt')
        self.thread_launch = None
        self.thread_shutdown = None

        self.load_account_file()
        self.load_combo_box()

    def closeEvent(self, event):
        print("close event")
        print("closed")

    def add_account(self):
        print("add account")
        add_account.AddAccountDialog.getWinInfo(self)
        self.qcombobox_account.clear()
        self.load_account_file()
        self.load_combo_box()

    def change_steam_path(self):
        print("Change Steam path")
        steam_path.SteamPathDialog.getWinInfo(self)

    def remove_account(self):
        print("remove account")
        remove_account.RemoveAccountDialog.getWinInfo(self)
        self.qcombobox_account.clear()
        self.load_account_file()
        self.load_combo_box()

    def load_account_file(self):
        if not os.path.exists(self.filename):
            f = open(self.filename, 'w')
            f.close()
        else:
            self.account_dic = {}

            f = open(self.filename, "r+")

            for line in f.readlines():
                username, password = line.split(' ')
                self.account_dic[username] = [username, password]

            f.close()

    def load_combo_box(self):
        if len(self.account_dic) == 0:
            self.qcombobox_account.addItem("No account(s) registered !")
        for key in self.account_dic.keys():
            self.qcombobox_account.addItem(key)

    def launch_steam(self):
        login, password = self.account_dic[self.qcombobox_account.currentText()]

        password = password.replace('\n', '')

        steam_thread = SteamThread.SteamThread_launch(login, password)
        steam_thread.start()

        self.thread_launch = steam_thread

    def connect(self):
        thread_shut = SteamThread.SteamThread_shutdown()
        thread_shut.start()

        thread_shut.wait()

        self.launch_steam()

    def main_window_signal_manager(self):
        # manage all signal send by the main window or main gui
        # like refresh or about
        # row = None
        # if self.table.selectionModel().selection().indexes():
        #     for i in self.table.selectionModel().selection().indexes():
        #         row, column = i.row(), i.column()

        # if self.sender() == self.parent().aboutAction:
        #     print("about")
        #     self.aboutPopUp()

        pass

    def aboutPopUp(self):
        mailLabel = QLabel("<a href='mailto:ponceau.nathanael@gmail.com'>ponceau.nathanael@gmail.com</a>")
        mailLabel.setOpenExternalLinks(True)

        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setText("Steam Account Manager is created by : \n Nathanael Ponceau")
        msg.layout().addWidget(mailLabel)
        msg.setWindowTitle("About")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()


def resource_path(relative_path):
    '''
    Using this function to get the path of bundled resource into .exe with pyinstaller.
    ref:https://www.reddit.com/r/learnpython/comments/4kjie3/how_to_include_gui_images_with_pyinstaller/
    :param relative_path:
    :return:
    '''
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
