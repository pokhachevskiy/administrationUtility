from UserListWindow import *
from DataBaseWrapper import *
from Connection import *
from AuthorizationWindow import *

app = QApplication([])


# Выполняет переход на главный экран после процедуры авторизации.
class Router:
    def __init__(self, creds):
        self.creds = creds

    def routeMainScreen(self):
        self.window = UserListWindow()
        self.connection = Connection(creds)
        database = self.obtain_database()
        self.window.database = database
        self.window.configure()
        self.window.show()

    def obtain_database(self):
        if test_mode:
            res = DataBaseWrapper()
            return res
        else:
            search_string = "(objectCategory=User)"
            res = self.connection.search(search_string)
            return res


creds = {}

router = Router(creds)

authorizationWindow = AuthorizationWindow(router, creds)
authorizationWindow.show()

app.exec_()
