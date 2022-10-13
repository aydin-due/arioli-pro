class User:
    def __init__(self, name, username, password):
        self.name = name
        self.username = username
        self.password = password
    
    def toBDCollection(self):
        return {
            "name": self.name,
            "username": self.username,
            "password": self.password
        }