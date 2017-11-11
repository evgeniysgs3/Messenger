class BadRequestFromClientError(Exception):
    def __init__(self, username):
        self.username = username

    def __str__(self):
        return 'Плохой запрос от клиента {}'.format(self.username)