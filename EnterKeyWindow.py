from PyQt5.QtWidgets import *
import sys

from PyQt5.uic.properties import QtGui

from KeyService import *
from Encoder import *


# Окно ввода ключа шифрования
class EnterKeyWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """

    def __init__(self, encoder, delegate) -> QWidget:
        super().__init__()
        self.encoder = encoder
        self.delegate = delegate
        self.key_was_added = False
        self.vert_layout = QVBoxLayout()

        self.button = QPushButton()
        self.button.setText("OK")
        self.button.clicked.connect(self.button_clicked)

        self.lineEdit = QLineEdit()
        self.lineEdit.setPlaceholderText("ключ шифрования")

        self.label = QLabel("Введите ключ шифрования ГОСТ 34.12-2018 Кузнечик")

        self.vert_layout.addWidget(self.label)
        self.vert_layout.addWidget(self.lineEdit)

        self.vert_layout.addWidget(self.button)
        self.setLayout(self.vert_layout)

    def button_clicked(self):
        try:
            self.encoder.set_key(bytes.fromhex(self.lineEdit.text()))
            self.key_was_added = True
            self.close()
        except:
            msg = QMessageBox()
            self.msg = msg
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Ключ не является корректным шестнадцатиричным представлением ключа шифрования для шифра ГОСТ 34.12-2018 Кузнечик")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.show()

    def closeEvent(self, event):
        if self.key_was_added:
            self.delegate.set_mode(2)
        else:
            self.delegate.set_mode(0)
        event.accept()
