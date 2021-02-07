from PyQt5.QtGui import *
from UserAttributesWindow import *
from DataBaseWrapper import *
from EnterKeyWindow import *
from environment import test_mode


# Главное окно приложения.
# Окно списка пользователей домена.
class UserListWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        wid = QWidget(self)
        self.setCentralWidget(wid)
        self.database = []
        self.encoder = Encoder()
        self.attributes_map = AttributesMap('config_plain.json')
        self.encoder.set_mode(False)
        layout = QVBoxLayout()
        self.encryption_mode_box = QCheckBox("Защищенный режим")
        self.amdz_login_enabled_box = QCheckBox("Разрешен вход в АМДЗ")
        self.filter_state = False

        self.list = QListView()
        # self.line = QLineEdit()
        self.model = QStandardItemModel(self.list)
        self.list.doubleClicked.connect(self.show_user_attributes_window)

        self.encryption_mode_box.stateChanged.connect(self.encryption_mode_changed)
        self.amdz_login_enabled_box.stateChanged.connect(self.filter_mode_changed)

        layout.addWidget(self.encryption_mode_box)
        layout.addWidget(self.list)
        layout.addWidget(self.amdz_login_enabled_box)
        # layout.addWidget(self.line)
        wid.setLayout(layout)
        self.list.setWindowTitle('Users')
        self.list.setMinimumSize(600, 400)

    def filter_mode_changed(self, state):
        self.filter_state = state != 0
        self.configure(state != 0)

    def encryption_mode_changed(self, state):
        if state != 0:
            self.show_encryption_key_input_window()
        self.set_mode(state)

    def set_mode(self, mode):
        self.encryption_mode_box.setChecked(mode != 0)
        self.encoder.set_mode(mode != 0)
        if not self.encoder.mode:
            self.attributes_map = AttributesMap('config_plain.json')
        else:
            self.attributes_map = AttributesMap('config.json')
        self.configure(self.filter_state)

    def show_encryption_key_input_window(self):
        self.encryption_key_input_window = EnterKeyWindow(self.encoder, self)
        self.encryption_key_input_window.show()

    def show_user_attributes_window(self, index):
        self.w = UserAttributesWindow(self.model.itemFromIndex(index).data(), self.encoder, self.attributes_map)
        self.w.delegate = self.database
        self.w.show()

    def configure(self, filter_enabled=False):
        self.model.clear()
        if test_mode:
            items = self.process_items(self.database.data['users'], filter_enabled)
        else:
            items = self.process_items(self.database, filter_enabled)
        self.update_model_with_items(items)

    def create_item(self, text, data):
        item = QStandardItem(text)
        item.setData(data)
        item.setEditable(False)
        return item

    def process_items(self, db, filter_enabled=False):
        model_items = []
        key = self.attributes_map.amap['amdzLoginEnabled']
        for elem in db:
            wrap = DictWrapper(elem)
            if filter_enabled:
                try:
                    value = elem[key]
                    if isinstance(value, list):
                        value = value[0]
                    value = str(value)
                    state = self.encoder.decrypt(bytes.fromhex(value)).decode()
                    # print(state)
                    if int(state) == 0:
                        continue
                except:
                    continue
            sAMAccountName = str(elem['sAMAccountName'][0])
            model_items.append(self.create_item(sAMAccountName, wrap))
        return model_items

    def update_model_with_items(self, items):
        for item in items:
            self.model.appendRow(item)
        # Apply the model to the list view
        self.list.setModel(self.model)