from PyQt5.QtGui import *
from UserAttributesWindow import *


class UserListWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        wid = QWidget(self)
        self.setCentralWidget(wid)
        self.database = []
        layout = QVBoxLayout()
        self.list = QListView()
        self.line = QLineEdit()
        self.model = QStandardItemModel(self.list)
        self.list.doubleClicked.connect(self.show_new_window)
        layout.addWidget(self.list)
        layout.addWidget(self.line)
        wid.setLayout(layout)

    def show_new_window(self, index):
        self.w = UserAttributesWindow(self.model.itemFromIndex(index).data())
        self.w.delegate = self.database
        self.w.show()

    def configure(self):
        self.list.setWindowTitle('Users')
        self.list.setMinimumSize(600, 400)

    def update_model_with_items(self, items):
        for item in items:
            self.model.appendRow(item)
        # Apply the model to the list view
        self.list.setModel(self.model)