from PyQt5.QtWidgets import *
import sys
from KeyService import *
from Encoder import *
from NamedLineEdit import NamedLineEdit


class UserAttributesWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """

    def __init__(self, data) -> QWidget:
        super().__init__()
        self.data = data.data
        self.delegate = []
        self.attributes = {'Имя пользователя': 'amdzUserName', 'Группа': 'amdzGroup'}
        try:
            key = KeyService().key
            self.encoder = Encoder(key)
        except:
            self.encoder = None
        self.vert_layout = QVBoxLayout()
        self.button = QPushButton()
        self.button.setText("Внести изменения")
        self.status = QLabel()
        self.formLayout = QFormLayout()
        self.table = {}

        self.label = QLabel(str(self.data["sAMAccountName"][0]))
        self.vert_layout.addWidget(self.label)

        self.create_table()
        self.vert_layout.addLayout(self.formLayout)
        self.vert_layout.addWidget(self.button)
        self.vert_layout.addWidget(self.status)
        self.setLayout(self.vert_layout)
        self.setup()

    def create_table(self):
        form_layout = self.formLayout
        for attribute in self.attributes:
            line = self.create_label(attribute)
            line.text_was_changed.connect(self.update_database)
            form_layout.addRow(str(attribute), line)
            self.table[attribute] = line

    def update_database(self, attribute, text):
        self.data[attribute] = [self.encoder.encrypt(text.encode('utf-8')).hex()]
        # print(self.data)

    def create_label(self, attribute):
        line = NamedLineEdit(self.attributes[attribute])
        try:
            value = self.data[self.attributes[attribute]]
            if isinstance(value, list):
                value = value[0]
            data = self.encoder.decrypt(bytes.fromhex(value)).decode()
            line.setText(data)
        except:
            line.setText("placeholder")
        return line

    def setup(self):
        self.button.clicked.connect(self.button_clicked)

    def button_clicked(self, button):
        try:
            self.delegate.modify()
            # self.data.modify()
            self.status.setText("accepted")
        except:
            print("exception")
            self.status.setText(str(sys.exc_info()[0]))
