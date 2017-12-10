class MaxMsgLengthExceedError(Exception):
    def __init__(self, username):
        self.username = username

    def __str__(self):
        return 'Пользователь {} привысил максимальная длину сообщения'.format(self.username)


class NoRequiredParameterActionError(Exception):
    def __str__(self):
        return 'В сообщении не присутствует обязательный параметр "action"'
