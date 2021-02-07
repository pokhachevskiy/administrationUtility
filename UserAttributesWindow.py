from PyQt5.QtWidgets import *
import sys
from KeyService import *
from Encoder import *
import json
from NamedLineEdit import NamedLineEdit
from NamedCheckBox import *
from AttributesMap import AttributesMap
from environment import test_mode

# Вспомогательные описания сложных атриубутов, содержащих более 1 строкового значения.
# Например, password_params
password_params = {"timeleft": "Время действия",
                   "minlength": "Минимальная длина",
                   "retries_left": "Попыток для смены"}

password_change_params = {"userMayChange": "Кто может менять пароль"}
alphabet_attrs = {'digits': {'name': 'Цифры', 'value': 1},
                'cchars': {'name': 'Заглавные латинские буквы', 'value': 2},
                'schars': {'name': 'Строчные латинские буквы', 'value': 4},
                'special': {'name': 'Специальные символы', 'value': 8},
                'onlygen': {'name': 'Только генерировать', 'value': 16}}
default_params = {"timeleft": "0", "minlength": "0", "retries_left": "0", "userMayChange": "0"}
admin_attrs = {'users': {'name': 'Редактирование пользователей', 'value': 1},
               'check': {'name': 'Редактирование контроля', 'value': 2},
               'log': {'name': 'Управление журналом', 'value': 4},
               'service': {'name': 'Редактирование настроек', 'value': 8}}
ia_attrs = {'tmid': {'name': 'Идентификатор', 'value': 1},
            'ws_secret_key': {'name': 'Секретный ключ станции', 'value': 2},
            'secret_key': {'name': 'Секретный ключ пользователя', 'value': 4},
            'name': {'name': 'Имя пользователя', 'value': 8},
            'password': {'name': 'Пароль', 'value': 16},
            'os_flags': {'name': 'Флаги ОС', 'value': 32},
            'recno': {'name': 'Номер пользователя', 'value': 64},
            'level': {'name': 'Уровень доступа пользователя', 'value': 128}}


# Окно отображения пользовательских атрибутов
class UserAttributesWindow(QWidget):

    def __init__(self, data, encoder, attributes_map) -> QWidget:
        super().__init__()
        widget = QWidget()
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
        widget.setLayout(self.vert_layout)

        scroll = QScrollArea()
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setMinimumWidth(750)
        scroll.setMinimumHeight(700)
        scroll.setWidget(widget)

        vLayout = QVBoxLayout(self)
        vLayout.addWidget(scroll)
        self.setLayout(vLayout)
        self.setup()

    def create_table(self):
        form_layout = self.formLayout
        for attribute in self.attributes:
            if self.attributes[attribute]['boolean']:
                view = self.create_checkbox(attribute)
                view.state_was_changed.connect(self.update_database)
            else:
                if self.attributes[attribute]['complex']:
                    view = self.create_complex_attribute(attribute)
                else:
                    view = self.create_label(attribute)
                    view.text_was_changed.connect(self.update_database)
            try:
                form_layout.addRow(str(attribute), view)
            except:
                pass

    def create_complex_attribute(self, attribute):
        date_picker_attributes = ['amdzActiveAfter', 'amdzActiveBefore', 'amdzPasswordExpirationDate']
        spinbox_attributes = ['amdzPasswordChangeRetriesLeft', 'amdzMaxAuthFails', 'amdzGroupFlag']
        view = []
        if self.attributes[attribute]['name'] in date_picker_attributes:
            view = self.create_date_picker_for_attribute(attribute)
            view.date_was_changed.connect(self.update_database)
        elif self.attributes[attribute]['name'] == 'amdzPasswordParams':
            view = self.create_password_params()
        elif self.attributes[attribute]['name'] == 'amdzAdminAttrs':
            view = self.create_admin_attributes()
        elif self.attributes[attribute]['name'] == 'amdzIaResults':
            view = self.create_ia_results()
        elif self.attributes[attribute]['name'] in spinbox_attributes:
            view = self.create_valued_box(attribute)
            if self.attributes[attribute]['name'] == 'amdzGroupFlag':
                view.setMaximum(255)
            view.value_was_changed.connect(self.update_database)
        return view

    def create_admin_attributes(self):
        admin_attributes_layout = QFormLayout()
        attribute = self.attributes['Привилегии администратора']
        key = attribute['value']
        current_attributes = 0
        try:
            current_attributes = self.data[key]
            if isinstance(current_attributes, list):
                current_attributes = current_attributes[0]
            current_attributes = int(self.decrypt(current_attributes))
        except:
            current_attributes = 0
        for param in admin_attrs:
            view = NamedCheckBox(param)
            condition = current_attributes & admin_attrs[param]['value'] == admin_attrs[param]['value']
            view.setChecked(condition)
            view.state_was_changed.connect(self.update_attrs_database)
            admin_attributes_layout.addRow(admin_attrs[param]['name'], view)
        return admin_attributes_layout

    def update_attrs_database(self, param, value):
        added_value = admin_attrs[param]['value']
        attribute = self.attributes['Привилегии администратора']
        key = attribute['value']
        try:
            current_attributes = self.data[key]
            if isinstance(current_attributes, list):
                current_attributes = current_attributes[0]
            current_attributes = int(self.decrypt(current_attributes))
        except:
            current_attributes = 0
        current_attributes ^= added_value
        casted_text = str(current_attributes)
        self.data[key] = [self.encrypt(casted_text)]


    def create_ia_results(self):
        ia_results_layout = QFormLayout()
        attribute = self.attributes['Результаты процедуры ИА']
        key = attribute['value']
        current_attributes = 0
        try:
            current_attributes = self.data[key]
            if isinstance(current_attributes, list):
                current_attributes = current_attributes[0]
            current_attributes = int(self.decrypt(current_attributes))
        except:
            current_attributes = 0
        for param in ia_attrs:
            view = NamedCheckBox(param)
            condition = current_attributes & ia_attrs[param]['value'] == ia_attrs[param]['value']
            view.setChecked(condition)
            view.state_was_changed.connect(self.update_ia_results_database)
            ia_results_layout.addRow(ia_attrs[param]['name'], view)
        return ia_results_layout

    def update_ia_results_database(self, param, value):
        added_value = ia_attrs[param]['value']
        attribute = self.attributes['Результаты процедуры ИА']
        key = attribute['value']
        try:
            current_attributes = self.data[key]
            if isinstance(current_attributes, list):
                current_attributes = current_attributes[0]
            current_attributes = int(self.decrypt(current_attributes))
        except:
            current_attributes = 0
        current_attributes ^= added_value
        casted_text = str(current_attributes)
        self.data[key] = [self.encrypt(casted_text)]

    def create_valued_box(self, attribute):
        key = self.attributes[attribute]['value']
        box = self.create_spinbox(key, 0)
        try:
            value = self.data[key]
            if isinstance(value, list):
                value = value[0]
            data = self.decrypt(value)
            box.setValue(int(data))
        except:
            box.setValue(0)
        return box

    def create_password_params(self):
        password_layout = QFormLayout()
        current_params = {}
        try:
            current_params = self.read_password_database()
        except:
            current_params = default_params
        for param in password_params:
            view = self.create_spinbox(param, current_params[param])
            view.value_was_changed.connect(self.update_password_database)
            password_layout.addRow(password_params[param], view)
        name = password_change_params["userMayChange"]
        value = 0
        try:
            value = current_params["userMayChange"]
        except:
            value = 0
        view = self.create_change_password_box(value)
        password_layout.addRow(name, view)

        alphabet_layout = self.create_generation_params(current_params)
        password_layout.addRow("Алфавит пароля", alphabet_layout)
        return password_layout

    def create_generation_params(self, current_params):
        alphabet_layout = QFormLayout()
        key = "password_alphabet"
        current_attributes = 0
        try:
            current_attributes = current_params[key]
        except:
            current_attributes = 0
        for param in alphabet_attrs:
            view = NamedCheckBox(param)
            condition = current_attributes & alphabet_attrs[param]['value'] == alphabet_attrs[param]['value']
            view.setChecked(condition)
            view.state_was_changed.connect(self.update_generation_database)
            alphabet_layout.addRow(alphabet_attrs[param]['name'], view)
        return alphabet_layout

    def update_generation_database(self, param, value):
        added_value = alphabet_attrs[param]['value']
        current_params = {}
        try:
            current_params = self.read_password_database()
        except:
            current_params = default_params
        key = "password_alphabet"
        try:
            current_attributes = int(current_params[key])
        except:
            current_attributes = 0
        current_attributes ^= added_value
        self.update_password_database(key, current_attributes)

    def create_change_password_box(self, value):
        vboxLayout = QVBoxLayout()
        groupBox = QGroupBox()
        radio_admin = QRadioButton("Только администратор")
        radio_user = QRadioButton("Пользователь и администратор")
        radio_admin.toggled.connect(lambda: self.change_password_policy_tapped(radio_admin))
        radio_user.toggled.connect(lambda: self.change_password_policy_tapped(radio_user))
        value = int(value)
        radio_admin.setChecked(value == 0)
        radio_user.setChecked(value == 1)
        vboxLayout.addWidget(radio_admin)
        vboxLayout.addWidget(radio_user)
        groupBox.setLayout(vboxLayout)
        return groupBox

    def change_password_policy_tapped(self, button):
        if button.text() == "Только администратор" and button.isChecked():
            self.update_password_database("userMayChange", 0)
        else:
            self.update_password_database("userMayChange", 1)

    def create_spinbox(self, key_name, value):
        box = NamedSpinBox(key_name)
        box.setMaximum(999)
        box.setValue(int(value))
        return box

    def create_date_picker_for_attribute(self, attribute):
        key = self.attributes[attribute]['value']
        date_picker = NamedDateEdit(key)
        date_picker.setMinimumWidth(100)
        try:
            value = self.data[key]
            if isinstance(value, list):
                value = value[0]
            value = str(value)
            date_string = self.decrypt(value)
            date = QDate.fromString(date_string, 'dd/MM/yyyy')
        except:
            date = QDate.currentDate()
        date_picker.setDate(date)
        return date_picker

    def create_checkbox(self, attribute):
        key = self.attributes[attribute]['value']
        checkbox = NamedCheckBox(key)
        try:
            value = self.data[key]
            if isinstance(value, list):
                value = value[0]
            state = int(self.decrypt(value))
        except:
            state = False
        checkbox.setChecked(bool(int(state)))
        return checkbox

    def encrypt(self, text):
        return self.encoder.encrypt(text.encode('utf-8')).hex()

    def decrypt(self, text):
        value = str(text)
        data = self.encoder.decrypt(bytes.fromhex(value)).decode()
        return data

    def read_password_database(self):
        attribute = self.attributes['Параметры пароля']
        key = attribute['value']
        old = self.data[key]
        if isinstance(old, list):
            old = old[0]
        current_params_json_str = self.decrypt(old)
        current_params_json = json.loads(current_params_json_str)
        return current_params_json

    def update_password_database(self, parameter_key, value):
        attribute = self.attributes['Параметры пароля']
        key = attribute['value']
        try:
            current_params_json = self.read_password_database()
        except:
            current_params_json = json.loads(json.dumps(default_params))
        current_params_json = current_params_json
        current_params_json[parameter_key] = value
        self.data[key] = [self.encrypt(json.dumps(current_params_json))]

    def update_database(self, attribute, text):
        casted_text = str(text)
        self.data[attribute] = [self.encrypt(casted_text)]
        # print(self.data)

    def create_label(self, attribute):
        key = self.attributes[attribute]['value']
        line = NamedLineEdit(key)
        line.setMinimumWidth(180)
        try:
            value = self.data[key]
            if isinstance(value, list):
                value = value[0]
            data = self.decrypt(value)
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
            self.status.setText("Изменения внесены успешно!")
        except AttributeError as err:
            print(err)
            self.status.setText("Произошла ошибка")
        except:
            self.status.setText("Произошла ошибка записи в БД: " + str(sys.exc_info()))
