from UserListWindow import *
from DataBaseWrapper import *
from Connection import *


app = QApplication([])


def create_item(text, data):
    item = QStandardItem(text)
    item.setData(data)
    item.setEditable(False)
    return item

def obtain_database():
    search_string = "(objectCategory=User)"
    res = connection.search(search_string)
    return res
    # database = DataBaseWrapper()

def process_items(database):
    items = []
    for elem in database:
        wrap = DictWrapper(elem)
        sAMAccountName = str(elem['sAMAccountName'][0])
        items.append(create_item(sAMAccountName, wrap))
    return items


creds = {'domain': "domain.ru", 'user': "sdz@domain.ru", 'password': "p@ssw0rd"}
credsa = {'domain': "domain.ru", 'user': "Administrator", 'password': "Xpe79qa81v1"}


connection = Connection(creds)
# connection.database = database

window = UserListWindow()

window.configure()
database = obtain_database()
items = process_items(database)
window.database = database

window.update_model_with_items(items)

# Show the window and run the app

window.show()
app.exec_()
