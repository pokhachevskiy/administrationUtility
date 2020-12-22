from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class NamedLineEdit(QLineEdit):
    text_was_changed = pyqtSignal(str, str)

    def __init__(self, name):
        super().__init__()
        self.name = name
        self.textChanged.connect(self.text_did_changed)

    def text_did_changed(self, text):
        self.text_was_changed.emit(self.name, self.text())
