import json


class DictWrapper:
    def __init__(self, data):
        self.data = data


# Обертка над базой данных для отладочного режима (не требует домена в окружении)
class DataBaseWrapper:
    def __init__(self):
        try:
            db = open('db.json', 'r')
            # Reading from json file
            dict_db = json.load(db)
            db.close()
        except:
            db = open('db.json', 'w')
            dict_db = {'users': [{'sAMAccountName': ["test1"], 'amdzUserName': ["2134134"], 'amdzGroup': ["group"]},
                                 {'sAMAccountName': ["test2"], 'amdzUserName': ["213adfadsf4134"],
                                  'amdzGroup': ["group"]}]}
            json_object = json.dumps(dict_db)
            db.write(json_object)
            db.close()
        self.data = dict_db

    def modify(self):
        db = open('db.json', 'w')
        json_object = json.dumps(self.data)
        db.write(json_object)
        db.close()
        print(self.data)
