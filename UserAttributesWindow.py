from PyQt5.QtWidgets import *
import sys
from KeyService import *
from Encoder import *
from NamedLineEdit import NamedLineEdit
from NamedCheckBox import NamedCheckBox
from AttributesMap import AttributesMap
from environment import test_mode


class UserAttributesWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """

    def __init__(self, data, encoder, attributes_map) -> QWidget:
        super().__init__()
        self.data = data.data
        self.delegate = []
        # start with password and kind of work (enc/noenc)
        self.attributes = attributes_map.attributes
        self.encoder = encoder

        self.vert_layout = QVBoxLayout()
        self.button = QPushButton()
        self.button.setText("Внести изменения")
        self.status = QLabel()
        self.formLayout = QFormLayout()

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
            if self.attributes[attribute]['boolean']:
                view = self.create_checkbox(attribute)
                view.state_was_changed.connect(self.update_database)
            else:
                view = self.create_label(attribute)
                view.text_was_changed.connect(self.update_database)
            form_layout.addRow(str(attribute), view)

    def create_checkbox(self, attribute):
        key = self.attributes[attribute]['value']
        checkbox = NamedCheckBox(key)
        try:
            value = self.data[key]
            if isinstance(value, list):
                value = value[0]
            value = str(value)
            state = self.encoder.decrypt(bytes.fromhex(value)).decode()
        except:
            state = False
        checkbox.setChecked(bool(int(state)))
        return checkbox

    def update_database(self, attribute, text):
        casted_text = str(text)
        self.data[attribute] = [self.encoder.encrypt(casted_text.encode('utf-8')).hex()]
        # print(self.data)

    def create_label(self, attribute):
        key = self.attributes[attribute]['value']
        line = NamedLineEdit(key)
        line.setMinimumWidth(180)
        try:
            value = self.data[key]
            if isinstance(value, list):
                value = value[0]
            value = str(value)
            data = self.encoder.decrypt(bytes.fromhex(value)).decode()
            line.setText(data)
        except (UnicodeDecodeError, IndexError):
            line.setPlaceholderText("Значение повреждено")
        except:
            line.setPlaceholderText("Значение не установлено")
        return line

    def setup(self):
        self.button.clicked.connect(self.button_clicked)

    def button_clicked(self, button):
        try:
            if test_mode:
                self.delegate.modify()
            else:
                self.data.modify()
            self.status.setText("accepted")
        except AttributeError as err:
            print(err)
            self.status.setText("Произошла ошибка")
        except:
            self.status.setText("Произошла ошибка записи в БД: " + str(sys.exc_info()))
