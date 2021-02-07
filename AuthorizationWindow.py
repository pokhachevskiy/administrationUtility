from PyQt5.QtWidgets import *
from Connection import *
import sys


# Окно авторизации пользователя
class AuthorizationWindow(QWidget):

    def __init__(self, router, creds) -> QWidget:
        super().__init__()
        self.creds = creds
        self.router = router

        self.vert_layout = QVBoxLayout()
        self.hor_layout = QHBoxLayout()

        self.login_button = QPushButton()
        self.login_button.setText("OK")
        self.login_button.clicked.connect(self.button_login_clicked)

        self.cancel_button = QPushButton()
        self.cancel_button.setText("Отмена")
        self.cancel_button.clicked.connect(self.button_cancel_clicked)

        self.login = QLineEdit()
        self.login.setPlaceholderText("Логин")
        self.login_label = QLabel("Логин администратора домена")

        self.password = QLineEdit()
        self.password_label = QLabel("Пароль администратора домена")
        self.password.setPlaceholderText("Пароль")
        self.password.setEchoMode(QLineEdit.Password)

        self.status = QLabel("Введите логин и пароль, затем нажмите ОК.")

        self.vert_layout.addWidget(self.login_label)
        self.vert_layout.addWidget(self.login)

        self.vert_layout.addWidget(self.password_label)
        self.vert_layout.addWidget(self.password)
        self.vert_layout.addWidget(self.status)

        self.hor_layout.addWidget(self.cancel_button)
        self.hor_layout.addWidget(self.login_button)

        self.vert_layout.addLayout(self.hor_layout)
        self.setLayout(self.vert_layout)

    def button_login_clicked(self):
        self.creds['user'] = self.login.text()
        self.creds['password'] = self.password.text()
        self.creds['domain'] = "domain.ru"

        try:
            conn = Connection(self.creds)
            self.router.routeMainScreen()
            self.close()
        except:
            self.status.setText("Пароль или логин не верны. Попробуйте еще раз.")

    def button_cancel_clicked(self):
        self.close()
