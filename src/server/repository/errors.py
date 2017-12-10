# Ошибки сервера


class NoneClientError(Exception):
    def __init__(self, username):
        self.username = username

    def __str__(self):
        return 'Пользователь {} не зарегистрирован'.format(
            self.username)
