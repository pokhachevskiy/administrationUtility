from UserListWindow import *
from DataBaseWrapper import *
from Connection import *

app = QApplication([])


def obtain_database():
    if test_mode:
        res = DataBaseWrapper()
        return res
    else:
        search_string = "(objectCategory=User)"
        res = connection.search(search_string)
        return res


creds_file = open('credentials.json', 'r')
creds = json.load(creds_file)
creds_file.close()


window = UserListWindow()
connection = Connection(creds)

database = obtain_database()


# connection.database = database

window.database = database

window.configure()

window.show()
app.exec_()
