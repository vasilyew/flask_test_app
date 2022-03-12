class IncorrectLoginOrPassword(Exception):
    def __init__(self):
        self.txt = 'Incorrect login or password'


class UserAlreadyExists(Exception):
    def __init__(self):
        self.txt = 'User already exists'


class UserIsNotFound(Exception):
    def __init__(self):
        self.txt = 'User is not found'


class SessionIsNotFound(Exception):
    def __init__(self):
        self.txt = 'Session is not found'