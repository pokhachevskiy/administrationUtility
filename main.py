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
    # search_string = "(objectCategory=User)"
    # res = connection.search(search_string)
    # return res
    res = DataBaseWrapper()
    return res


def process_items(db):
    model_items = []
    for elem in db:
        wrap = DictWrapper(elem)
        sAMAccountName = str(elem['sAMAccountName'][0])
        model_items.append(create_item(sAMAccountName, wrap))
    return model_items


creds_file = open('credentials.json', 'r')
creds = json.load(creds_file)
creds_file.close()


window = UserListWindow()

window.configure()
database = obtain_database()

window.database = database

connection = Connection(creds)
connection.database = database


window.configure()

items = process_items(database.data['users'])
window.update_model_with_items(items)


window.show()
app.exec_()
