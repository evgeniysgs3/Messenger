# Ошибки клиента


class NoneContactError(Exception):
    def __init__(self, username):
        self.username = username

    def __str__(self):
        return 'Пользователя {} нет в списке контактов'.format(
            self.username)
