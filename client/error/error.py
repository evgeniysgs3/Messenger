#  все ошибки


class UsernameToLongError(Exception):
    def __init__(self, username):
        self.username = username

    def __str__(self):
        return 'Имя пользователя {} должно быть менее 26 символов'.format(
            self.username)


class MandatoryKeyError(Exception):
    def __init__(self, key):
        self.key = key

    def __str__(self):
        return 'Не хватает обязательного атрибута {}'.format(self.key)


class ServerAvailabilityError(Exception):
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def __str__(self):
        return 'Сервер IP:{} PORT:{} не доступен'.format(self.ip, self.port)