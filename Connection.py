# import bonsai


class Connection:
    def __init__(self, credentials):
        self.database = []
        domain = credentials['domain']
        user = credentials['user']
        password = credentials['password']

        # self.client = bonsai.LDAPClient("ldap://" + domain)
        # self.client.set_credentials("SIMPLE", user=user, password=password)
        # self.connection = self.client.connect(timeout=10)

    def search(self, text):
        # res = self.connection.search("dc=domain,dc=ru", 2, text)
        # return res
        return self.database.data['users']

