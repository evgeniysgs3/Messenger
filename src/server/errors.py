class BadRequestFromClientError(Exception):
    def __init__(self, rem_ip):
        self.rem_ip = rem_ip

    def __str__(self):
        return 'Плохой запрос от клиента {}'.format(self.rem_ip)

class ClientDisconected(Exception):
    def __init__(self, rem_ip):
        self.rem_ip = rem_ip

    def __str__(self):
        return 'Клиент {} отключился'.format(self.rem_ip)