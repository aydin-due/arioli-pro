class User:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
        self.admin = False
    
    def toBDCollection(self):
        return {
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "admin": self.admin
        }