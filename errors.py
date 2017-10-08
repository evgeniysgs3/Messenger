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


class BadRequestFromClientError(Exception):
    def __init__(self, username):
        self.username = username

    def __str__(self):
        return 'Плохой запрос от клиента {}'.format(self.username)


class MaxMsgLengthExceedError(Exception):
    def __init__(self, username):
        self.username = username

    def __str__(self):
        return 'Пользователь {} привысил максимальная длину сообщения'.format(self.username)
