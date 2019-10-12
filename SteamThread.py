# Import the core and GUI elements of Qt
from PyQt5.QtCore import QThread
import psutil
import os
from pathlib import Path
import subprocess


class SteamThread_launch(QThread):

    def __init__(self, username, password):
        QThread.__init__(self)
        self.username = username
        self.password = password

        local_program_folder_path = os.path.normpath(
            os.path.normpath(Path.home()) + "\AppData\Local\SteamAccountManager")
        self.filename = os.path.join(local_program_folder_path, 'steam_path.txt')

        self.steam_path = None
        self.load_steam_path_file()

    def __del__(self):
        self.wait()

    def run(self):
        self.launch_steam(self.username, self.password)

    def launch_steam(self, login, password):
        subprocess.run([self.steam_path, "-login", login, password], shell=False)

    def load_steam_path_file(self):
        f = open(self.filename, "r+")

        for line in f.readlines():
            self.steam_path = line.replace('\n', '')

        f.close()


class SteamThread_shutdown(QThread):

    def __init__(self):
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    def run(self):
        self.kill_steam()

    def kill_steam(self):
        PROCNAME = "Steam.exe"

        for proc in psutil.process_iter():
            if proc.name() == PROCNAME:
                proc.terminate()
