from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class NamedCheckBox(QCheckBox):
    state_was_changed = pyqtSignal(str, int)

    def __init__(self, name):
        super().__init__()
        self.name = name
        self.stateChanged.connect(self.state_did_changed)

    def state_did_changed(self, state):
        self.state_was_changed.emit(self.name, state)
