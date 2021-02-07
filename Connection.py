from environment import test_mode

if not test_mode:
    import bonsai


# Класс отвечающий за подключение оператора к базе данных AD
class Connection:
    def __init__(self, credentials):
        domain = credentials['domain']
        user = credentials['user']
        password = credentials['password']

        if not test_mode:
            self.client = bonsai.LDAPClient("ldap://" + domain)
            self.client.set_credentials("SIMPLE", user=user, password=password)
            self.connection = self.client.connect(timeout=10)

    def search(self, text):
        res = self.connection.search("dc=domain,dc=ru", 2, text)
        return res


