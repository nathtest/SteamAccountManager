from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLineEdit, QToolButton, QStyle, QDateEdit
import os
import sys


class ButtonLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super(ButtonLineEdit, self).__init__(parent)

        self.button = QToolButton(self)
        self.button.setIcon(QIcon(resource_path("Resource/Grey_close_x.png")))
        self.button.setIconSize(QSize(12, 12))
        self.button.setStyleSheet('border: 0px; padding: 0px;')
        self.button.setCursor(Qt.ArrowCursor)
        self.button.setToolTip("Clear text")
        self.button.clicked.connect(self.clear)

        frameWidth = self.style().pixelMetric(QStyle.PM_DefaultFrameWidth)
        buttonSize = self.button.sizeHint()

        self.setStyleSheet('QLineEdit {padding-right: %dpx; }' % (buttonSize.width() + frameWidth + 1))
        self.setMinimumSize(max(self.minimumSizeHint().width(), buttonSize.width() + frameWidth * 2 + 2),
                            max(self.minimumSizeHint().height(), buttonSize.height() + frameWidth * 2 + 2))

    def resizeEvent(self, event):
        buttonSize = self.button.sizeHint()
        frameWidth = self.style().pixelMetric(QStyle.PM_DefaultFrameWidth)
        self.button.move(self.rect().right() - frameWidth - buttonSize.width(),
                         (self.rect().bottom() - buttonSize.height() + 1) / 2)
        super(ButtonLineEdit, self).resizeEvent(event)


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
